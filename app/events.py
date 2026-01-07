from flask import session, request
from flask_socketio import emit, join_room, leave_room
from services.matchmaking_service import MatchmakingService

def register_events(socketio):
    @socketio.on('connect')
    def on_connect():
        with open('debug.log', 'a') as f:
            f.write(f"CONNECT EVENT: Session: {session}\n")
        
        user = session.get('user_data')
        if not user:
            with open('debug.log', 'a') as f:
                 f.write("CONNECT REJECTED: No user\n")
            return False # Reject
        with open('debug.log', 'a') as f:
             f.write(f"User {user.get('Username')} connected.\n")
        print(f"User {user.get('Username')} connected.")

    @socketio.on('find_match')
    def on_find_match():
        with open('debug.log', 'a') as f:
            f.write("FIND_MATCH EVENT\n")
            
        user = session.get('user_data')
        user = session.get('user_data')
        username = user.get('Username')
        user_id = user.get('Id')
        
        result = MatchmakingService.find_match(user_id)
        room_id = result.get('id')
        status = result.get('status')
        
        join_room(room_id)
        
        if status == 'MATCH_FOUND':
            # Notify both players that game starts
            # Need to get questions first
            room_state = MatchmakingService.get_room_state(room_id)
            questions = room_state.get('DatosPartida', [])
            
            # Emit to the room (both players)
            emit('game_start', {
                'roomId': room_id,
                'questions': questions,
                'opponent': 'Opponent' # In future fetch names
            }, room=room_id)
        else:
            emit('waiting_for_opponent', {'roomId': room_id})

    @socketio.on('player_update')
    def on_player_update(data):
        # Relay status (e.g., "Thinking...", "Typing...") to opponent in room
        # data: { roomId: '...', status: 'Thinking' }
        room_id = data.get('roomId')
        user = session.get('user_data')
        emit('opponent_update', {
            'username': user.get('Username'),
            'status': data.get('status'),
            'progress': data.get('progress')
        }, room=room_id, include_self=False)

    @socketio.on('round_submit')
    def on_round_submit(data):
        # data: { roomId: '...', round: 1, correct: true/false }
        room_id = data.get('roomId')
        is_correct = data.get('correct')
        user = session.get('user_data')
        
        # In a real impl, we shouldn't trust client 'correct' flag, 
        # but for this demo we trust frontend validation or we re-validate here.
        # Let's trust for now as per "Watch then Do" request flow.
        
        # If wrong -> Eliminated (Sudden Death)
        if not is_correct:
            emit('game_over', {
                'winner': 'Opponent', 
                'reason': f"{user.get('Username')} missed a question!"
            }, room=room_id)
            # Verify if this closes room or not
        else:
             # Just notify progress
             emit('opponent_update', {
                'username': user.get('Username'),
                'status': 'CORRECT_ANSWER',
                'round': data.get('round')
             }, room=room_id, include_self=False)

