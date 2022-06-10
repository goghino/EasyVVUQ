"""Analysis element for polynomial chaos expansion (PCE). We use ChaosPy
under the hood for this functionality.
"""
import logging
import chaospy as cp
import numpy as np
import numpoly
import warnings
from easyvvuq import OutputType
from .base import BaseAnalysisElement
from .results import AnalysisResults
from .qmc_analysis import QMCAnalysisResults

__author__ = 'Jalal Lakhlili'
__license__ = "LGPL"

logger = logging.getLogger(__name__)


class PCEAnalysisResults(QMCAnalysisResults):
    """Analysis results for the PCEAnalysis class.
    """

    def _get_derivatives_first(self, qoi, input_):
        """Returns the first order derivative-based index for a given qoi wrt input variable.

        Parameters
        ----------
        qoi : str
           Quantity of interest
        input_ : str
           Input variable

        Returns
        -------
        float
            First order derivative-based index.
        """

        raw_dict = AnalysisResults._keys_to_tuples(self.raw_data['derivatives_first'])
        return raw_dict[AnalysisResults._to_tuple(qoi)][input_]

    def _get_sobols_first(self, qoi, input_):
        """Returns the first order sobol index for a given qoi wrt input variable.

        Parameters
        ----------
        qoi : str
           Quantity of interest
        input_ : str
           Input variable

        Returns
        -------
        float
            First order sobol index.
        """
        raw_dict = AnalysisResults._keys_to_tuples(self.raw_data['sobols_first'])
        return raw_dict[AnalysisResults._to_tuple(qoi)][input_]

    def _get_sobols_second(self, qoi, input_):
        """Returns the second order sobol index for a given qoi wrt input variable.

        Parameters
        ----------
        qoi : str
           Quantity of interest
        input_ : str
           Input variable

        Returns
        -------
        float
            Second order sobol index.
        """
        raw_dict = AnalysisResults._keys_to_tuples(self.raw_data['sobols_second'])
        return dict([(in_, raw_dict[AnalysisResults._to_tuple(qoi)][input_][i])
                     for i, in_ in enumerate(self.inputs) if in_ != input_])

    def _get_sobols_total(self, qoi, input_):
        """Returns the total order sobol index for a given qoi wrt input variable.

        Parameters
        ----------
        qoi : str
           Quantity of interest
        input_ : str
           Input variable

        Returns
        -------
        float
            Total order sobol index.
        """
        raw_dict = AnalysisResults._keys_to_tuples(self.raw_data['sobols_total'])
        return raw_dict[AnalysisResults._to_tuple(qoi)][input_]

    def supported_stats(self):
        """Types of statistics supported by the describe method.

        Returns
        -------
        list of str
        """
        return ['min', 'max', '10%', '90%', '1%', '99%', 'median',
                'mean', 'var', 'std']

    def _describe(self, qoi, statistic):
        """Returns descriptive statistics, similar to pandas describe.

        Parameters
        ----------
        qoi : str
            Name of quantity of interest.
        statistic : str
            One of 'min', 'max', '10%', '90%', 'median', 'mean', 'var', 'std'

        Returns
        -------
        float
            Value of the requested statistic.
        """
        if statistic not in self.supported_stats():
            raise NotImplementedError
        if statistic == 'min':
            return np.array([v.lower[0] for _, v in enumerate(
                self.raw_data['output_distributions'][qoi])])
        elif statistic == 'max':
            return np.array([v.upper[0] for _, v in enumerate(
                self.raw_data['output_distributions'][qoi])])
        elif statistic == '1%':
            return self.raw_data['percentiles'][qoi]['p01']
        elif statistic == '10%':
            return self.raw_data['percentiles'][qoi]['p10']
        elif statistic == '90%':
            return self.raw_data['percentiles'][qoi]['p90']
        elif statistic == '99%':
            return self.raw_data['percentiles'][qoi]['p99']
        elif statistic == 'median':
            return self.raw_data['percentiles'][qoi]['p50']
        else:
            try:
                return self.raw_data['statistical_moments'][qoi][statistic]
            except KeyError:
                raise NotImplementedError

    def surrogate(self):
        """Return a PCE surrogate model.

        Returns
        -------
        A function that takes a dictionary of parameter - value pairs and returns
        a dictionary with the results (same output as decoder).
        """
        def surrogate_fn(inputs):
            def swap(x):
                if len(x) > 1:
                    return list(x)
                else:
                    return x[0]
            values = np.array([inputs[key] for key in self.inputs])
            results = dict([(qoi, swap((self.raw_data['fit'][qoi](*values)).T))
                           for qoi in self.qois])
            return results
        return surrogate_fn

    def get_distribution(self, qoi):
        """Returns a distribution for the given qoi.

        Parameters
        ----------
        qoi: str
            QoI name

        Returns
        -------
        A ChaosPy PDF
        """
        if qoi not in self.qois:
            raise RuntimeError('no such quantity of interest - {}'.format(qoi))
        return self.raw_data['output_distributions'][qoi]


class PCEAnalysis(BaseAnalysisElement):

    def __init__(self, sampler=None, qoi_cols=None, sampling=False):
        """Analysis element for polynomial chaos expansion (PCE).

        Parameters
        ----------
        sampler : PCESampler
            Sampler used to initiate the PCE analysis.
        qoi_cols : list or None
            Column names for quantities of interest (for which analysis is
            performed).
        sampling : True if chaospy sampling method to be used for calculating
            statitical quantities; otherwise [default] the pce coefficients are used
        """

        if sampler is None:
            msg = 'PCE analysis requires a paired sampler to be passed'
            raise RuntimeError(msg)

        # Flag specifing if we should scale the runs with the nominal base run
        self.relative_analysis = sampler.relative_analysis

        if qoi_cols is None:
            raise RuntimeError("Analysis element requires a list of "
                               "quantities of interest (qoi)")

        self.qoi_cols = qoi_cols
        self.sampling = sampling
        self.output_type = OutputType.SUMMARY
        self.sampler = sampler

    def element_name(self):
        """Name for this element for logging purposes.

        Returns
        -------
        str
            "PCE_Analysis"
        """
        return "PCE_Analysis"

    def element_version(self):
        """Version of this element for logging purposes.

        Returns
        -------
        str
            Element version.
        """
        return "0.6"

    def analyse(self, data_frame=None):
        """Perform PCE analysis on input `data_frame`.

        Parameters
        ----------
        data_frame : pandas DataFrame
            Input data for analysis.

        Returns
        -------
        PCEAnalysisResults
            Use it to get the sobol indices and other information.
        """

        def sobols(P, coefficients):
            """ Utility routine to calculate sobols based on coefficients
            """
            A = np.array(P.coefficients) != 0
            multi_indices = np.array([P.exponents[A[:, i]].sum(axis=0) for i in range(A.shape[1])])
            sobol_mask = multi_indices != 0
            _, index = np.unique(sobol_mask, axis=0, return_index=True)
            index = np.sort(index)
            sobol_idx_bool = sobol_mask[index]
            sobol_idx_bool = np.delete(sobol_idx_bool, [0], axis=0)
            n_sobol_available = sobol_idx_bool.shape[0]
            if len(coefficients.shape) == 1:
                n_out = 1
            else:
                n_out = coefficients.shape[1]
            n_coeffs = coefficients.shape[0]
            sobol_poly_idx = np.zeros([n_coeffs, n_sobol_available])
            for i_sobol in range(n_sobol_available):
                sobol_poly_idx[:, i_sobol] = np.all(sobol_mask == sobol_idx_bool[i_sobol], axis=1)
            sobol = np.zeros([n_sobol_available, n_out])
            for i_sobol in range(n_sobol_available):
                sobol[i_sobol] = np.sum(
                    np.square(coefficients[sobol_poly_idx[:, i_sobol] == 1]), axis=0)
            idx_sort_descend_1st = np.argsort(sobol[:, 0], axis=0)[::-1]
            sobol = sobol[idx_sort_descend_1st, :]
            sobol_idx_bool = sobol_idx_bool[idx_sort_descend_1st]
            sobol_idx = [0 for _ in range(sobol_idx_bool.shape[0])]
            for i_sobol in range(sobol_idx_bool.shape[0]):
                sobol_idx[i_sobol] = np.array(
                    [i for i, x in enumerate(sobol_idx_bool[i_sobol, :]) if x])
            var = ((coefficients[1:]**2).sum(axis=0))
            sobol = sobol / (var + np.finfo(float).tiny)
            return sobol, sobol_idx, sobol_idx_bool

        def build_surrogate_der(Y_hat, verbose=False):
            '''Computes derivative of the polynomial Y_hat w.r.t. Vars
            Parameter T specifies the time dimension
            '''

            #TODO: build derivative only with respect to a subset of variables
            dim = len(self.sampler.vary.vary_dict)
            Vars = [v.names[0] for v in cp.variable(dim)]
            T = len(Y_hat)

            assert(len(Vars) == len(self.sampler.vary.vary_dict))

            # derivative of the PCE expansion
            # {dYhat_dx1: [t0, t1, ...],
            #  dYhat_dx2: [t0, t1, ...],
            #  ...,
            #  dYhat_dxN: [t0, t1, ...] }
            #TODO: Vars can be simplified to simple array of strings ['qi'] instad of {'qi': poly('qi')}
            dY_hat = {v:[cp.polynomial(0) for t in range(T)] for v in self.sampler.vary.vary_dict}

            for t in range(T):

                for n1, n2 in zip(Y_hat[t].names, Vars):
                    assert(n1 == n2)

                for d_var_idx, (d_var, d_var_app) in enumerate(zip(Vars, self.sampler.vary.vary_dict)):

                    if verbose:
                        print(f'Computing derivative d(Y_hat)/d({d_var})')
                        print('='*40)

                    # Some variables are missing in the expression,
                    # then they must be constant terms only i.e. sum(exp==0)
                    if Y_hat[t].exponents.shape[1] < dim:
                        #exponents.shape: (n_summands, n_variables)
                        assert(sum(sum(np.array(Y_hat[t].exponents))) == 0)
                        continue
                        #print(Y_hat[t])
                        #print(Y_hat[t].exponents)
                        #print(d_var_idx)

                    # Consider only polynomial components var^exp where exp > 0 (since the derivative decreases exp by -1)
                    # 306 ms ± 5.97 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
                    components_mask = np.array(Y_hat[t].exponents[:,d_var_idx] > 0)
                    dY_hat_dvar_exp = Y_hat[t].exponents[components_mask]
                    dY_hat_dvar_coeff = np.array(Y_hat[t].coefficients)[components_mask]

                    # 911 ms ± 24 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
                    #dY_hat_dvar_exp   = [exp for exp in Y_hat[t].exponents if exp[d_var_idx] > 0]
                    #dY_hat_dvar_coeff = [Y_hat[t].coefficients[i] for i, exp in enumerate(Y_hat[t].exponents) if exp[d_var_idx] > 0]

                    # Iterate over all polynomial components (summands)
                    for i, (coeff, exp) in enumerate(zip(dY_hat_dvar_coeff, dY_hat_dvar_exp)):
                        assert(exp[d_var_idx] > 0)

                        # derivative = coeff*exp * var^(exp-1)
                        dY_hat_dvar_coeff[i] = coeff * exp[d_var_idx]
                        dY_hat_dvar_exp[i][d_var_idx] = exp[d_var_idx] - 1

                    dY_hat[d_var_app][t] = numpoly.construct.polynomial_from_attributes(
                                exponents=dY_hat_dvar_exp,
                                coefficients=dY_hat_dvar_coeff,
                                names=Y_hat[t].names,
                                retain_coefficients=True,
                                retain_names=True)

            return dY_hat

        if data_frame is None:
            raise RuntimeError("Analysis element needs a data frame to "
                               "analyse")
        elif data_frame.empty:
            raise RuntimeError(
                "No data in data frame passed to analyse element")

        qoi_cols = self.qoi_cols
        T = len(data_frame[qoi_cols[0]].values[-1])

        results = {'statistical_moments': {k: {'mean':np.zeros(T),
                                               'var':np.zeros(T),
                                               'std':np.zeros(T)} for k in qoi_cols},
                   'percentiles': {k: {'p01': np.zeros(T),
                                       'p10': np.zeros(T),
                                       'p50': np.zeros(T),
                                       'p90': np.zeros(T),
                                       'p99': np.zeros(T)} for k in qoi_cols},
                   'sobols_first': {k: {p: np.zeros(T) for p in self.sampler.vary.vary_dict} for k in qoi_cols},
                   'sobols_second': {k: {p: np.zeros(T) for p in self.sampler.vary.vary_dict} for k in qoi_cols},
                   'sobols_total': {k: {p: np.zeros(T) for p in self.sampler.vary.vary_dict} for k in qoi_cols},
                   'correlation_matrices': {k: {} for k in qoi_cols},
                   'output_distributions': {k: {} for k in qoi_cols},
                   'fit': {k: cp.polynomial(np.zeros(T)) for k in qoi_cols},
                   'Fourier_coefficients': {k: {p: np.zeros(T) for p in self.sampler.vary.vary_dict} for k in qoi_cols},
                   'derivatives_first': {k: {p: np.zeros(T) for p in self.sampler.vary.vary_dict} for k in qoi_cols},
                   }

        # Get sampler informations
        P = self.sampler.P
        nodes = self.sampler._nodes
        weights = self.sampler._weights
        regression = self.sampler.regression

        # Extract output values for each quantity of interest from Dataframe
#        samples = {k: [] for k in qoi_cols}
#        for run_id in data_frame[('run_id', 0)].unique():
#            for k in qoi_cols:
#                data = data_frame.loc[data_frame[('run_id', 0)] == run_id][k]
#                samples[k].append(data.values.flatten())

        samples = {k: [] for k in qoi_cols}
        for k in qoi_cols:
            if self.relative_analysis:
                base = data_frame[k].values[-1]
                if np.all(np.array(base) == 0):
                    warnings.warn(f"Removing QoI {k} from the analysis, contains all zeros", RuntimeWarning)
                    continue

                # Scale the model output to make it relative to the base run
                samples[k] = data_frame[k].values[:-1] / base - 1
            else:
                samples[k] = data_frame[k].values
            
            #print(f'Original {data_frame[k].values[:-1] = }')
            #print(f'Base run {data_frame[k].values[-1] = }')
            #print(f'Scaled {samples[k] = }')

            # Compute descriptive statistics for each quantity of interest
            if regression:
                fit, fc = cp.fit_regression(P, nodes, samples[k], retall=1)
            else:
                fit, fc = cp.fit_quadrature(P, nodes, weights, samples[k], retall=1)
            results['fit'][k] = fit
            results['Fourier_coefficients'][k] = fc

            # Percentiles: 1%, 10%, 50%, 90% and 99%
            P01, P10, P50, P90, P99 = cp.Perc(
                fit, [1, 10, 50, 90, 99], self.sampler.distribution).squeeze()
            results['percentiles'][k] = {'p01': P01, 'p10': P10, 'p50': P50, 'p90': P90, 'p99': P99}

            if self.sampling:  # use Chaospy's sampling method

                # Statistical moments
                mean = cp.E(fit, self.sampler.distribution)
                var = cp.Var(fit, self.sampler.distribution)
                std = cp.Std(fit, self.sampler.distribution)
                results['statistical_moments'][k] = {'mean': mean,
                                                     'var': var,
                                                     'std': std}

                # Sensitivity Analysis: First, Second and Total Sobol indices
                #TODO: there is a bug when the sensitivity indices computed
                # using Sens_m2() and Sens_t() are recursively calling itself
                # infinitely, check the Chaospy implementation of these functions!
                print(f'Warning: second and total order indices computed using \
                        PCEAnalysis(sampling = True) might result in infinite  \
                        recusion due to the Chaospy\'s implementation!!!' )
                sobols_first_narr = cp.Sens_m(fit, self.sampler.distribution)
                sobols_second_narr = cp.Sens_m2(fit, self.sampler.distribution)
                sobols_total_narr = cp.Sens_t(fit, self.sampler.distribution)
                sobols_first_dict = {}
                sobols_second_dict = {}
                sobols_total_dict = {}
                for i, param_name in enumerate(self.sampler.vary.vary_dict):
                    sobols_first_dict[param_name] = sobols_first_narr[i]
                    sobols_second_dict[param_name] = sobols_second_narr[i]
                    sobols_total_dict[param_name] = sobols_total_narr[i]

                results['sobols_first'][k] = sobols_first_dict
                results['sobols_second'][k] = sobols_second_dict
                results['sobols_total'][k] = sobols_total_dict

            else:  # use PCE coefficients

                # Statistical moments
                mean = fc[0]
                var = np.sum(fc[1:]**2, axis=0)
                std = np.sqrt(var)
                results['statistical_moments'][k] = {'mean': mean,
                                                     'var': var,
                                                     'std': std}

                # Sensitivity Analysis: First, Second and Total Sobol indices
                sobol, sobol_idx, _ = sobols(P, fc)
                varied = [_ for _ in self.sampler.vary.get_keys()]
                S1 = {_: np.zeros(sobol.shape[-1]) for _ in varied}
                ST = {_: np.zeros(sobol.shape[-1]) for _ in varied}
                # S2 = {_ : {__: np.zeros(sobol.shape[-1]) for __ in varied} for _ in varied}
                # for v in varied: del S2[v][v]
                S2 = {_: np.zeros((len(varied), sobol.shape[-1])) for _ in varied}
                for n, si in enumerate(sobol_idx):
                    if len(si) == 1:
                        v = varied[si[0]]
                        S1[v] = sobol[n]
                    elif len(si) == 2:
                        v1 = varied[si[0]]
                        v2 = varied[si[1]]
                        # S2[v1][v2] = sobol[n]
                        # S2[v2][v1] = sobol[n]
                        S2[v1][si[1]] = sobol[n]
                        S2[v2][si[0]] = sobol[n]
                    for i in si:
                        ST[varied[i]] += sobol[n]

                results['sobols_first'][k] = S1
                results['sobols_second'][k] = S2
                results['sobols_total'][k] = ST

            # Sensitivity Analysis: Derivative based
            dY_hat = build_surrogate_der(fit, verbose=False)
            derivatives_first_dict = {}
            Ndimensions = len(self.sampler.vary.vary_dict)
            for i, param_name in enumerate(self.sampler.vary.vary_dict):
                # Evaluate dY_hat['param'] at the origin
                derivatives_first_dict[param_name] = cp.polynomial(dY_hat[param_name])(*np.zeros(Ndimensions))

            results['derivatives_first'][k] = derivatives_first_dict

            # Correlation matrix
            try:
                warnings.warn(f"Skipping computation of cp.Corr", RuntimeWarning)
                results['correlation_matrices'][k] = None #cp.Corr(fit, self.sampler.distribution)
                    #TODO: if dependent, we want to return correlation of the self.sampler.distribution_dep?
            except Exception as e:
                print ('Error %s for %s when computing cp.Corr()'% (e.__class__.__name__, k))
                results['correlation_matrices'][k] = None
            

            # Output distributions
            try:
                warnings.warn(f"Skipping computation of cp.QoI_Dist", RuntimeWarning)
                results['output_distributions'][k] = None #cp.QoI_Dist( fit, self.sampler.distribution)
                    #TODO: When a multivariate distribution is dependent, it means that the pdf and
                    # cdf can only be defined together. If you want to define only one, than you
                    # have to "marginalize", which implies that you are loosing the dependency
                    # relationship. https://github.com/jonathf/chaospy/issues/339
            except Exception as e:
                print ('Error %s for %s when computing cp.QoI_Dist()'% (e.__class__.__name__, k))
#                from traceback import print_exc
#                print_exc()
                results['output_distributions'][k] = None

        return PCEAnalysisResults(raw_data=results, samples=data_frame,
                                  qois=self.qoi_cols, inputs=list(self.sampler.vary.get_keys()))
