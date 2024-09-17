from util.enums import MoveAction, PlayerEnum, HallEnum, RoomEnum

DUMMY_MOVE_ID = "0001"  # Dummy ID

move0 = MoveAction(PlayerEnum.prof_plum, RoomEnum.billiard, DUMMY_MOVE_ID)

move1 = MoveAction(PlayerEnum.prof_plum, HallEnum.hall_to_lounge, DUMMY_MOVE_ID)

move2 = MoveAction(PlayerEnum.prof_plum, RoomEnum.study, DUMMY_MOVE_ID)

move3 = MoveAction(PlayerEnum.prof_plum, RoomEnum.kitchen, DUMMY_MOVE_ID)

move4 = MoveAction(PlayerEnum.prof_plum, HallEnum.dining_to_kitchen, DUMMY_MOVE_ID)

move5 = MoveAction(PlayerEnum.mr_green, RoomEnum.ballroom, DUMMY_MOVE_ID)

move6 = MoveAction(PlayerEnum.mr_green, HallEnum.ballroom_to_kitchen, DUMMY_MOVE_ID)

MOVES = [move0, move1, move2, move3, move4, move5, move6]
