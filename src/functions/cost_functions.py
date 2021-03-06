import numpy as np

# Quadratic cost function
class QuadraticCost:
    @staticmethod
    def cost (network_output, expected_output):
        return sum(0.5*(np.power(network_output-expected_output, 2)))

    @staticmethod
    def delta (network_output, z_activation_deriv, expected_output):
        if expected_output.dtype == np.int:
            expected_output = np.asfarray(expected_output, dtype='float')
        return 0.5*(np.power(network_output-expected_output, 2)*z_activation_deriv)

# Optimized with softmax
class NegativeLogLikelihood:
    # returns the KL divergence
    @staticmethod
    def cost (network_output, expected_output):
        totalsum = 0.0
        for no, eo in zip(network_output,expected_output):
            if eo > 0:
                totalsum -= eo*np.log((no+0.0)/(eo+0.0))
        return totalsum

    @staticmethod
    def delta (network_output, z_activation_deriv, expected_output):
        if expected_output.dtype == np.int:
            expected_output = np.asfarray(expected_output, dtype='float')
        return network_output-expected_output
        #return -(expected_output/network_output)*z_activation_deriv

class CrossEntropy:
    @staticmethod
    def cost(network_output, expected_output):
        totalsum = 0.0
        for no, eo in zip(network_output, expected_output):
            if eo == 0:
                totalsum -= np.log(1.0-no)
            elif eo == 1:
                totalsum -= np.log(no)
            else:
                totalsum -= eo*np.log(no/eo) + (1.0-eo)*np.log((1.0-no)/(1.0-eo))
        return totalsum

    @staticmethod
    def delta(network_output, z_activation_deriv, expected_output):
        if expected_output.dtype == np.int:
            expected_output = np.asfarray(expected_output, dtype='float')
        return network_output - expected_output

class CustomCost:
    @staticmethod
    def cost (network_output, expected_output):
        return NegativeLogLikelihood.cost(network_output[:7], expected_output[:7]) \
               + QuadraticCost.cost(network_output[7:], expected_output[7:])

    @staticmethod
    def delta (network_output, z_activation_deriv, expected_output):
        deltas = np.zeros(8)
        deltas[:7] = NegativeLogLikelihood.delta(network_output[:7], z_activation_deriv[:7], expected_output[:7])
        deltas[7:] = CrossEntropy.delta(network_output[7:], z_activation_deriv[7:], expected_output[7:])
        return deltas

