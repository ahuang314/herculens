import jax.numpy as jnp
from jaxtronomy.Util.jax_util import BilinearInterpolator, BicubicInterpolator


class Pixelated(object):
    """Source brightness defined on a fixed coordinate grid."""
    param_names = ['x_coords', 'y_coords', 'image']
    method_options = ['bilinear', 'bicubic']

    def __init__(self, method='bilinear'):
        self._method = method
        error_msg = "Invalid method. Must be either 'bilinear' or 'bicubic'."
        assert self._method in self.method_options, error_msg

    def function(self, x, y, x_coords, y_coords, image):
        """Interpolated evaluation of a pixelated source.

        Parameters
        ----------
        x, y : array-like
            Coordinates at which to evaluate the source.
        x_coords : 1D array
            Rectangular x-coordinate grid values.
        y_coords : 1D array
            Rectangular y-coordinate grid values.
        image : 2D array
            Source brightness at fixed coordinate grid positions.
        method : str
            Interpolation method, either 'bilinear' or 'bicubic'.

        """
        # Warning: assuming same pixel size across all the image! 
        pixel_area = (x_coords[0]-x_coords[1]) * (y_coords[0]-y_coords[1])
        if self._method == 'bilinear':
            interp = BilinearInterpolator(x_coords, y_coords, image)
        else:
            interp = BicubicInterpolator(x_coords, y_coords, image)
        # we normalize the interpolated array for correct units when evaluated by LensImage methods
        return interp(y, x).T / pixel_area
