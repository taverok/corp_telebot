class StateMachine:
    states = {}

    @classmethod
    def set_state(cls, user_id: int, state: str) -> None:
        cls.states.update({user_id: state})

    @classmethod
    def get_state(cls, user_id: int) -> str:
        return cls.states.get(user_id)

    @classmethod
    def remove_state(cls, user_id: int):
        cls.states.pop(user_id)
