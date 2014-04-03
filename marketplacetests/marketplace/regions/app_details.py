# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from marionette.by import By
from gaiatest.apps.base import Base


class Details(Base):

    _write_review_locator = (By.ID, 'add-review')
    _app_info_locator = (By.CSS_SELECTOR, '.detail .info')
    _first_review_locator = (By.CSS_SELECTOR, 'li:first-child .review-inner > span')
    _first_review_body_locator = (By.CSS_SELECTOR, 'li:first-child .body')
    _install_button_locator = (By.CSS_SELECTOR, '.detail .info button.product.install')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_present(*self._app_info_locator)

    @property
    def is_app_details_displayed(self):
        return self.is_element_displayed(*self._app_info_locator)

    @property
    def install_button_text(self):
        return self.marionette.find_element(*self._install_button_locator).text

    @property
    def first_review_body(self):
        return self.marionette.find_element(*self._first_review_body_locator).text

    @property
    def first_review_rating(self):
        return int(self.marionette.find_element(*self._first_review_locator).get_attribute('class')[-1])

    def tap_write_review(self):
        self.wait_for_element_present(*self._write_review_locator)
        write_review_button = self.marionette.find_element(*self._write_review_locator)
        # element.tap() isn't working here
        # Bug 878750 - el.tap() and click() do not work on "Write a review" button
        write_review_button.tap()
        from marketplacetests.marketplace.regions.review_box import AddReview
        return AddReview(self.marionette)

    def tap_purchase_button(self):
        self.marionette.find_element(*self._install_button_locator).tap()
        # Return payment object

        from marketplacetests.payment.app import Payment
        return Payment(self.marionette)
