from oscar.apps.partner.strategy import Available, UseFirstStockRecord, NoTax, Structured
from oscar.apps.partner.prices import FixedPrice
from oscar.core.loading import get_class, get_model

StockRecord = get_model('partner', 'StockRecord')


class StockNotRequired(object):
    """
    Availability policy mixin for use with the ``Structured`` base strategy.
    This mixin ensures that a product can only be bought if it has stock
    available (if stock is being tracked).
    """

    def availability_policy(self, product, stockrecord):
        return Available()

    def parent_availability_policy(self, product, children_stock):
        return Available()


class FakeStockRecord(object):
    """
    Stockrecord selection mixin for use with the ``Structured`` base strategy.
    This mixin picks the first (normally only) stockrecord to fulfil a product.

    This is backwards compatible with Oscar<0.6 where only one stockrecord per
    product was permitted.
    """

    def select_stockrecord(self, product):
        try:
            return StockRecord.objects.all()[0]
        except IndexError:
            return None


class Default(FakeStockRecord, StockNotRequired, NoTax, Structured):
    """
    Default stock/price strategy that uses the first found stockrecord for a
    product, ensures that stock is available (unless the product class
    indicates that we don't need to track stock) and charges zero tax.
    """

    def pricing_policy(self, product, stockrecord):
        """
        Return the appropriate pricing policy
        """
        pricing = FixedPrice('', 0, 0)
        pricing.retail = 0
        return pricing


class Selector(object):
    """
    Responsible for returning the appropriate strategy class for a given
    user/session.

    This can be called in three ways:

    #) Passing a request and user.  This is for determining
       prices/availability for a normal user browsing the site.

    #) Passing just the user.  This is for offline processes that don't
       have a request instance but do know which user to determine prices for.

    #) Passing nothing.  This is for offline processes that don't
       correspond to a specific user.  Eg, determining a price to store in
       a search index.

    """

    def strategy(self, request=None, user=None, **kwargs):
        """
        Return an instanticated strategy instance
        """
        # Default to the backwards-compatible strategy of picking the first
        # stockrecord but charging zero tax.
        return Default(request)


