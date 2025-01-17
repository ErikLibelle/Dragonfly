# This file is for strategy
import os
from util.objects import *
from util.routines import *
from util.tools import find_hits


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

        def KickoffInitiation(kickoff_type):
            # Initializes Kickoff
            print("Kickoff Initialized")
            if kickoff_type == 0:  # Wide Diagnonal / Corners
                if self.ball_local[1] > 0:
                    self.debugtext = "Kickoff off from: Right Wide Diagonal"  # Debug
                    print("Kickoff off from: Right Wide Diagnonal")  # Log
                    self.set_intent(kickoff())
                    return
                else:
                    self.debugtext = "Kickoff off from: Left Wide Diagonal"  # Debug
                    print("Kickoff off from: Left Wide Diagnonal")  # Log
                    self.set_intent(kickoff())
                    return
            elif kickoff_type == 1:  # Short Diagonal / Back Sides
                if self.ball_local[1] < 0:
                    self.debugtext = "Kicking off from: Right Short Diagonal"  # Debug
                    print("Kicking off from: Right Short Diagonal")  # Log
                    self.set_intent(kickoff_short())
                    return
                else:
                    self.debugtext = "Kicking off from: Left Short Diagonal"  # Debug
                    print("Kicking off from: Left Short Diagonal")  # Log
                    self.set_intent(kickoff_short())
                    return
            elif kickoff_type == 2:  # Middle / Back Middle
                self.debugtext = "Kicking off from: Middle"  # Debug
                print("Kicking off from: Middle")  # Log
                self.set_intent(kickoff_center())
                return
            else:
                self.debugtext = (
                    "Error KickoffInitiation Cannot recognize Kickoff Position"  # Debug
                )
                print(
                    "Error KickoffInitiation Cannot recognize Kickoff Position"
                )  # Log
                self.set_intent(kickoff())
                return

        # if self.kickoff_flag:
        #     self.set_intent(Kickoff())
        #     return
        if self.kickoff_flag:
            kickoff_type = self.getKickoffPosition(
                self.me.location
            )  # Gets Kickoff Location
            KickoffInitiation(kickoff_type)  # Starts Kickoff Routine
            self.clear_debug_lines()
            self.add_debug_line(
                "me_to_kickoff", self.me.location, self.ball.location, [0, 0, 255]
            )
            self.add_debug_line(
                "kickoff_to_goal",
                self.ball.location,
                self.foe_goal.location,
                [0, 0, 255],
            )
            print(f"Kicking Off | Type: {kickoff_type}")  # Log
            return

        # @TODO: Make a state engine that determines whether we are in offense, defense, or scramble

        # don't judge my default code, this is a placeholder for week 2
        # offense
        if (me.location - ball.location).magnitude() < (
            opponent.location - ball.location
        ).magnitude():
            if (me.location - self.foe_goal.location).magnitude() < (
                me.location - ball.location
            ).magnitude():
                self.set_intent(GoTo(self.friend_goal.location))
                return
            targets = {
                "at_opponent_goal": (self.foe_goal.left_post, self.foe_goal.right_post),
                "away_from_my_net": (
                    self.friend_goal.right_post,
                    self.friend_goal.left_post,
                ),
            }
            hits = find_hits(self, targets)
            if len(hits["at_opponent_goal"]) > 0:
                self.set_intent(hits["at_opponent_goal"][0])
                return
            # fall back to short shot
            self.set_intent(ShortShot(self.foe_goal.location))
            return
        # defense
        else:
            # boosts is a sorted list of large boosts by distance to friend goal
            boosts = [boost for boost in self.boosts if boost.active and boost.large]
            boosts.sort(
                key=lambda boost: (
                    boost.location - self.friend_goal.location
                ).magnitude()
            )

            if (
                ball.location - self.friend_goal.location
            ).magnitude() < 5120 and me.boost < 40:
                self.set_intent(GoTo(boosts[0].location))
                return
            targets = {
                "at_opponent_goal": (self.foe_goal.left_post, self.foe_goal.right_post),
                "away_from_my_net": (
                    self.friend_goal.right_post,
                    self.friend_goal.left_post,
                ),
            }
            hits = find_hits(self, targets)
            if len(hits["at_opponent_goal"]) > 0:
                self.set_intent(hits["at_opponent_goal"][0])
                return
            if len(hits["away_from_my_net"]) > 0:
                self.set_intent(hits["away_from_my_net"][0])
                return

            self.set_intent(GoTo(me.location + (me.location - ball.location) / 2))

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
