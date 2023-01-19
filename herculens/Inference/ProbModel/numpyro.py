# Defines the model of a strong lens
# 
# Copyright (c) 2022, herculens developers and contributors
# based on the ImSim module from lenstronomy (version 1.9.3)

__author__ = 'aymgal'


import jax
import numpyro
from numpyro import handlers
from numpyro.infer import util

from herculens.Inference.ProbModel.base_model import BaseProbModel


__all__ = ['NumpyroModel']


class NumpyroModel(BaseProbModel):
    """Defines a numpyro model based on a LensImage instance"""

    def log_prob(self, params):
        # returns the logarithm of the data likelihood
        # plus the logarithm of the prior
        log_prob, trace = util.log_density(self.model, (), {}, params)
        return log_prob
    
    def log_likelihood(self, params):
        # returns the logarithm of the data likelihood
        return util.log_likelihood(self.model, params, batch_ndims=0)['obs']

    def seeded_model(self, seed=0):
        return handlers.seed(self.model, jax.random.PRNGKey(seed))
    
    def get_trace(self, seed=0):
        return handlers.trace(self.seeded_model(seed=seed)).get_trace()

    def get_sample(self, seed=0):
        trace = self.get_trace(seed=seed)
        return {site['name']: site['value'] for site in trace.values() if not site['is_observed']}

    def draw_samples(self, num_samples, obs=None, seed=0):
        batch_ndims = 0 if num_samples else 1
        predictive = util.Predictive(handlers.condition(self.model, {'obs': obs}), 
                                     num_samples=num_samples, 
                                     batch_ndims=batch_ndims)
        return predictive(jax.random.PRNGKey(seed))

    def render_model(self):
        return numpyro.render_model(self.get_trace())
