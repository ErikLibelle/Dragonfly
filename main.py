# This file is for strategy

from util.objects import *
from util.routines import Kickoff, ShortShot, GoTo
from util.common import compare_vec_mag


class Bot(CommandAgent):
    intent_swaps = 0
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        me = self.me
        ball = self.ball
        opponent = self.foes[0]

        if self.get_intent() is not None:
            return

        self.intent_swaps += 1
        print('intent swaps', self.intent_swaps)

        if self.kickoff_flag:
            self.set_intent(Kickoff())
            return
        
        # offense
        # if compare_vec_mag(me.location - ball.location, opponent.location - ball.location) > 0:
        if (me.location - ball.location).magnitude() < (opponent.location - ball.location).magnitude():
            if (me.location - self.foe_goal.location).magnitude() < (me.location - ball.location).magnitude():
                self.set_intent(GoTo(self.friend_goal.location))
                return
            self.set_intent(ShortShot(self.foe_goal.location))
            return
        else:
            self.set_intent(GoTo(ball.location))

        # if kickoff, kick off
        # if within <x> seconds of kickoff, run strategy based on how the opponent is acting

        # OBJECTIVE: Push ball past opponent
        # run through strategy change conditions, set overall strategy to:
        # - DEFENSE
        # - OFFENSE
        # - SCRAMBLE

        # Valuable decision making context
        # - Opponent is moving toward ball
        # - Opponent recently hit ball
        # - Opponent is flipping
        # - Opponent has boost
        # - Opponent can shoot
        # - Estimated time to impact (self and opponent)
        # - Ball is on our net
        # - Ball is high in the air

        # DEFENSE
        # Context: We cannot hit ball before opponent
        # - Opponent has ball
        #   - Look for opportunity to turn and hit it
        #     - Opponent we are facing ball
        #     - Opponent low boost?
        #     - Opponent pushing ball
        #   - Get in between opponent and goal
        #     - Shadow if ball on ground
        #     - If we can tell that the opponent has just hit the ball, or has just flipped, see if ball is on net
        #       - If on net, jump to defend
        #       - If not on net, predict where it's going and plan a hit
        # - Opponent is far from ball
        #   - If moving toward ball
        #     - If we can beat them, plan a hit, even if it's toward our net
        #   - If we can't beat them, estimate time to possession
        #     - Move to "Opponent has ball" strategy if we can't beat them
        #     - Look to acquire position or boost in most effective manner before moving to "Opponent has ball" strategy

        # OFFENSE
        # Context: We can hit ball before opponent
        # Objective: Move ball up the field, or create a threatening situation
        # - If we have a CLEAR shot, plan a shot
        # - If opponent is coming toward ball, plan hit around them
        # - If opponent is guarding properly, hit against back wall

        # SCRAMBLE
        # Context: It is unclear whether we or the opponent are getting to the ball first
        # Objective: Position and acquire resources to make it more likely that we possess the ball

        # Open Questions
        # - Is there ever a scenario where we just wait for the opponent to screw up?
        # - Is there any low-hanging fruit that the bot can learn from (e.g. when the opponent takes shots,
        #   what they do after shots, where they get in bad position, etc...)
        # Can we know all of the info about our opponent?

