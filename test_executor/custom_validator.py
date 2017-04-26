from setting.models import CustomValidateRule


class CustomValidator:
    def __init__(self, rule_id):
        self.result = False
        self.error_msg = 'Unknown error!'
        self.custom_validate_rule = CustomValidateRule.objects.get(id=rule_id)

    def __call__(self, response_dict):
        result = False
        error_msg = 'Unknown error!'

        try:
            exec self.custom_validate_rule.code
        except Exception, e:
            result = False
            error_msg = e.message

        self.result = result
        if self.result:
            self.error_msg = ''
        else:
            self.error_msg = error_msg
        return self.result
