from torch import optim, nn

from ..models.model import Model
from ..utils import tolist
from ..losses import NLL


class ML(Model):
    def __init__(self, p,
                 other_distributions=[],
                 other_losses=None,
                 optimizer=optim.Adam,
                 optimizer_params={}):
        super().__init__()

        self.p = p
        self.other_distributions = nn.ModuleList(tolist(other_distributions))

        # set losses
        self.nll = NLL(self.p)
        self.other_losses = other_losses
        loss_cls = (self.nll + self.other_losses).mean()
        self.loss_cls = loss_cls
        self.test_loss_cls = loss_cls
        self.loss_text = str(loss_cls)

        # set params and optim
        p_params = list(self.p.parameters())
        other_params = list(self.other_distributions.parameters())
        params = p_params + other_params
        self.optimizer = optimizer(params, **optimizer_params)

    def train(self, train_x, **kwargs):
        self.p.train()
        self.other_distributions.train()

        return super().train(train_x, **kwargs)

    def test(self, test_x, **kwargs):
        self.p.eval()
        self.other_distributions.eval()

        return super().test(test_x, **kwargs)

