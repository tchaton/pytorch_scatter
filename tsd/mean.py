import torch

from tsd import scatter_add


def scatter_mean(src, index, dim=-1, out=None, dim_size=None, fill_value=0):
    r"""
    |

    .. image:: https://raw.githubusercontent.com/rusty1s/pytsd/
            master/docs/source/_figures/mean.svg?sanitize=true
        :align: center
        :width: 400px

    |

    Averages all values from the :attr:`src` tensor into :attr:`out` at the
    indices specified in the :attr:`index` tensor along a given axis
    :attr:`dim`.If multiple indices reference the same location, their
    **contributions average** (`cf.` :meth:`~tsd.scatter_add`).

    For one-dimensional tensors, the operation computes

    .. math::
        \mathrm{out}_i = \mathrm{out}_i + \frac{1}{N_i} \cdot
        \sum_j \mathrm{src}_j

    where :math:`\sum_j` is over :math:`j` such that
    :math:`\mathrm{index}_j = i`. :math:`N_i` indicates the number of indices
    referencing :math:`i`.

    Args:
        src (Tensor): The source tensor.
        index (LongTensor): The indices of elements to scatter.
        dim (int, optional): The axis along which to index.
            (default: :obj:`-1`)
        out (Tensor, optional): The destination tensor. (default: :obj:`None`)
        dim_size (int, optional): If :attr:`out` is not given, automatically
            create output with size :attr:`dim_size` at dimension :attr:`dim`.
            If :attr:`dim_size` is not given, a minimal sized output tensor is
            returned. (default: :obj:`None`)
        fill_value (int, optional): If :attr:`out` is not given, automatically
            fill output tensor with :attr:`fill_value`. (default: :obj:`0`)

    :rtype: :class:`Tensor`

    .. testsetup::

        import torch

    .. testcode::

        from tsd import scatter_mean

        src = torch.Tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
        index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])
        out = src.new_zeros((2, 6))

        out = scatter_mean(src, index, out=out)

        print(out)

    .. testoutput::

       tensor([[0.0000, 0.0000, 4.0000, 3.0000, 1.5000, 0.0000],
               [1.0000, 4.0000, 2.0000, 0.0000, 0.0000, 0.0000]])
    """
    out = scatter_add(src, index, dim, out, dim_size, fill_value)
    count = scatter_add(torch.ones_like(src), index, dim, None, out.size(dim))
    return out / count.clamp(min=1)
