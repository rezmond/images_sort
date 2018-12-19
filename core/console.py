# -*- coding: utf-8 -*-


class Console:
    NOT_TRUE_ANSWER_MSG = 'пожалуйста введите одно из следующих значений'

    def __init__(self, allowed_commands):
        super(Console, self).__init__()
        self._allowed_commands = allowed_commands

    @property
    def allowed_commands(self):
        return self._allowed_commands

    def get_quoted_allowed_commands(self):
        return map('"{}"'.format, self._allowed_commands)

    def ask_user(self, message):
        user_answer = input(message).lower()

        not_true_answer_msg = '{0}: {1}\n'.format(
            self.NOT_TRUE_ANSWER_MSG.capitalize(),
            ', '.join(self.get_quoted_allowed_commands)
        ).encode('utf-8')

        while user_answer not in self.allowed_commands:
            user_answer = input(not_true_answer_msg).lower()

        return user_answer


class ResolverConsole(Console):

    def __init__(self, true_commands, false_commands):
        super(ResolverConsole, self).__init__(true_commands + false_commands)
        self._true_commands = true_commands
        self._false_commands = false_commands

    def ask_user(self, message):
        result = super(ResolverConsole, self).ask_user(message)
        return result in self._true_commands
