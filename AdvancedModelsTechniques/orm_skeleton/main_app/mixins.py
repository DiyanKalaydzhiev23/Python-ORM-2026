class RechargeEnergyMixin:
    MAX_ENERGY: int = 100

    def recharge_energy(self, amount: int) -> None:
        self.energy = min(self.MAX_ENERGY, self.energy + amount)