import torch
from allennlp.common.checks import ConfigurationError


class Debiaser:
    """
    Parent class for bias debiaser classes.

    # Parameters

    requires_grad : `bool`, optional (default=`False`)
        Option to enable gradient calculation.
    """

    def __init__(self, requires_grad: bool = False):
        self.requires_grad = requires_grad


class HardDebiaser(Debiaser):
    """
    Hard debiaser. Debiases embeddings by:

    1. Neutralizing: ensuring protected variable-neutral words remain equidistant
    from the bias direction by removing component of embeddings
    in the bias direction.

    2. Equalizing: ensuring that protected variable-related words are averaged
    out to have the same norm.

    Description taken from: Goenka, D. (2020). [Tackling Gender Bias in Word Embeddings]
    (https://towardsdatascience.com/tackling-gender-bias-in-word-embeddings-c965f4076a10).

    Implementation based on Rathore, A., Dev, S., Phillips, J.M., Srikumar,
    V., Zheng, Y., Yeh, C.M., Wang, J., Zhang, W., & Wang, B. (2021).
    [VERB: Visualizing and Interpreting Bias Mitigation Techniques for
    Word Representations](https://api.semanticscholar.org/CorpusID:233168618).
    ArXiv, abs/2104.02797.
    """

    def forward(self, embeddings: torch.Tensor, bias_direction: torch.Tensor):
        """

        # Parameters

        embeddings : `torch.Tensor`
            A tensor of size (batch_size, ..., dim).
        bias_direction : `torch.Tensor`
            A unit tensor of size (dim, ) representing the concept subspace.

        # Returns

        debiased_embeddings : `torch.Tensor`
            A tensor of the same size as embeddings. debiased_embeddings do not contain a component
            in bias_direction.
        """

        with torch.set_grad_enabled(self.requires_grad):
            return embeddings - torch.matmul(
                embeddings, bias_direction.reshape(-1, 1)
            ) * bias_direction / torch.dot(bias_direction, bias_direction)


class LinearDebiaser(Debiaser):
    """
    Linear debiaser. Debiases embeddings by removing component
    in the bias direction.

    Implementation and terminology based on Rathore, A., Dev, S., Phillips, J.M., Srikumar,
    V., Zheng, Y., Yeh, C.M., Wang, J., Zhang, W., & Wang, B. (2021).
    [VERB: Visualizing and Interpreting Bias Mitigation Techniques for
    Word Representations](https://api.semanticscholar.org/CorpusID:233168618).
    ArXiv, abs/2104.02797.

    # Parameters

    requires_grad : `bool`, optional (default=`False`)
        Option to enable gradient calculation.
    """

    def forward(self, embeddings: torch.Tensor, bias_direction: torch.Tensor):
        """

        # Parameters

        embeddings : `torch.Tensor`
            A tensor of size (batch_size, ..., dim).
        bias_direction : `torch.Tensor`
            A unit tensor of size (dim, ) representing the concept subspace.

        # Returns

        debiased_embeddings : `torch.Tensor`
            A tensor of the same size as embeddings. debiased_embeddings do not contain a component
            in bias_direction.
        """
        with torch.set_grad_enabled(self.requires_grad):
            return (
                embeddings
                - torch.matmul(embeddings, bias_direction.reshape(-1, 1)) * bias_direction
            )
