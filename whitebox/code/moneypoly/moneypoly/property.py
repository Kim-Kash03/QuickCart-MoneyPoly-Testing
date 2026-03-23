"""
Property and group classes for the MoneyPoly game board.
"""
from dataclasses import dataclass

@dataclass
class PropertyConfig:
    """Configuration data for initializing a property."""
    name: str
    position: int
    price: int
    base_rent: int
    group: any = None

class Property:
    """Represents a single purchasable property tile on the MoneyPoly board."""

    FULL_GROUP_MULTIPLIER = 2

    @classmethod
    def create(cls, name, position, price, base_rent, group=None):
        """Create a new Property instance using positional arguments."""
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        return cls(PropertyConfig(name, position, price, base_rent, group))

    def __init__(self, config):
        self.config = config
        self.mortgage_value = self.config.price // 2
        self.owner = None
        self.is_mortgaged = False
        self.houses = 0

        # Register with the group immediately on creation
        if self.config.group is not None and self not in self.config.group.properties:
            self.config.group.properties.append(self)

    @property
    def name(self):
        """Return the name of the property."""
        return self.config.name

    @property
    def position(self):
        """Return the board position of the property."""
        return self.config.position

    @property
    def price(self):
        """Return the purchase price of the property."""
        return self.config.price

    @property
    def base_rent(self):
        """Return the base rent value of the property."""
        return self.config.base_rent

    @property
    def group(self):
        """Return the colour group of the property."""
        return self.config.group

    @group.setter
    def group(self, group_obj):
        self.config.group = group_obj

    def get_rent(self):
        """
        Return the rent owed for landing on this property.
        Rent is doubled if the owner holds the entire colour group.
        Returns 0 if the property is mortgaged.
        """
        if self.is_mortgaged:
            return 0
        if self.group is not None and self.group.all_owned_by(self.owner):
            return self.base_rent * self.FULL_GROUP_MULTIPLIER
        return self.base_rent

    def mortgage(self):
        """
        Mortgage this property and return the payout to the owner.
        Returns 0 if already mortgaged.
        """
        if self.is_mortgaged:
            return 0
        self.is_mortgaged = True
        return self.mortgage_value

    def unmortgage(self):
        """
        Lift the mortgage on this property.
        Returns the cost (110 % of mortgage value), or 0 if not mortgaged.
        """
        if not self.is_mortgaged:
            return 0
        cost = int(self.mortgage_value * 1.1)
        self.is_mortgaged = False
        return cost

    def is_available(self):
        """Return True if this property can be purchased (unowned, not mortgaged)."""
        return self.owner is None and not self.is_mortgaged

    def __repr__(self):
        owner_name = self.owner.name if self.owner else "unowned"
        return f"Property({self.name!r}, pos={self.position}, owner={owner_name!r})"


class PropertyGroup:
    """Represents a set of properties belonging to the same colour group."""
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.properties = []

    def add_property(self, prop):
        """Add a Property to this group and back-link it."""
        if prop not in self.properties:
            self.properties.append(prop)
            prop.group = self

    def all_owned_by(self, player):
        """Return True if every property in this group is owned by `player`."""
        if player is None:
            return False
        return all(p.owner == player for p in self.properties)

    def get_owner_counts(self):
        """Return a dict mapping each owner to how many properties they hold in this group."""
        counts = {}
        for prop in self.properties:
            if prop.owner is not None:
                counts[prop.owner] = counts.get(prop.owner, 0) + 1
        return counts

    def size(self):
        """Return the number of properties in this group."""
        return len(self.properties)

    def __repr__(self):
        return f"PropertyGroup({self.name!r}, {len(self.properties)} properties)"
