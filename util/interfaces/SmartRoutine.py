class SmartRoutine():
    last_check: int
    name: str
    # gets flipped to false on the first time the routine is run
    first_run: bool = True

    def run(self, agent: CommandAgent) -> None:
        pass
    
    def next_check(self) -> int:
        return 100