# -*- coding: utf-8 -*-

from typing import Any

from mapping import agreement, subscription
from . import generators


class Value:
    """Make random value for the attribute."""

    _func = {
        "prop": generators.prop,
        "site_name": generators.site,
        agreement.credit_schema_id.onyma_key: (generators.credit_schema),
        agreement.dog_date.onyma_key: generators.dog_date,
        agreement.dog_group_id.onyma_key: generators.gid,
        agreement.status.onyma_key: generators.status,
        agreement.customer_type.onyma_key: (generators.agreement_type),
        agreement.additional_email.onyma_key: (generators.email),
        agreement.additional_telephone.onyma_key: (generators.telephone),
        agreement.date_of_birth.onyma_key: (generators.passport_birthdate),
        agreement.email.onyma_key: generators.email,
        agreement.name.onyma_key: generators.name,
        agreement.number_sms_info.onyma_key: (generators.sms_telephone),
        agreement.passport_date_of_issue.onyma_key: (
            generators.passport_issued
        ),
        agreement.passport_issued_by.onyma_key: (
            generators.passport_issued_by
        ),
        agreement.passport_number.onyma_key: (generators.passport_number),
        agreement.passport_series.onyma_key: (generators.passport_series),
        agreement.passport_subdivision_code.onyma_key: (
            generators.passport_subdivision
        ),
        agreement.place_of_birth.onyma_key: (
            generators.passport_place_of_birth
        ),
        agreement.registration_address.onyma_key: (
            generators.passport_address
        ),
        agreement.telephone.onyma_key: generators.telephone,
        agreement.telephone_mobile.onyma_key: generators.telephone,
        subscription.hhid.onyma_key: generators.generate_hhid,
    }

    def new_value(self, attribute_key, old_value: Any = ""):
        """Return new value."""
        func = self._func.get(attribute_key)
        if func:
            return func(old_value)
        else:
            raise NotImplementedError
