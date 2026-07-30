"""General representation of a linear map using its basis images."""

class LinearMap:
    """
    Defines a general linear map L: R^d -> V, where V is a vector space.

    The map is represented by the images of the standard basis vectors:
    L(e_1), ..., L(e_d).

    Elements of V support addition and scalar multiplication.
    """

    def __init__(self, basis_images):
        """
        Define the linear map using its basis images.

        Parameters
        ----------
        basis_images:
            The sequence [L(e_1), ..., L(e_d)] determining the map.
        """
        self.basis_images = tuple(basis_images)

        if len(self.basis_images) == 0:
            raise ValueError("At least one basis image is required.")

        self.domain_dim = len(self.basis_images)

    @property
    def matrix_dim(self):
        """Return the size of the square basis-image matrices."""
        first_image = self.basis_images[0]

        if first_image.rows != first_image.cols:
            raise ValueError(
                "The basis images must be square matrices."
            )

        return first_image.rows

    def __call__(self, x):
        """
        Evaluate L(x) for x in R^d.

        Parameters: x = [x_1, ..., x_d] in R^d
        Returns: x_1 L(e_1) + ... + x_d L(e_d) in V
        """
        if len(x) != self.domain_dim:
            raise ValueError(
                f"Expected an input of dimension {self.domain_dim}. "
            )

        result = 0 * self.basis_images[0]

        for coefficient, image in zip(x, self.basis_images):
            result = result + coefficient * image

        return result

    def scaled(self, scalar):
        """
        Return the scaled linear map: scalar * L.
        The new map satisfies (scalar * L)(x) = scalar * L(x).
        """
        new_images = []

        for image in self.basis_images:
            new_images.append(scalar * image)

        return LinearMap(new_images)