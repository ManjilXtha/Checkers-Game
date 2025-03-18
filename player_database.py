import json
import os
from datetime import datetime

class PlayerDatabase:
    def __init__(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.save_folder = os.path.join(desktop_path, "CheckersSaveData")
        self.db_path = os.path.join(self.save_folder, "checkers_players.json")
        os.makedirs(self.save_folder, exist_ok=True)
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        if not os.path.exists(self.db_path):
            initial_data = {
                "players": [],
                "matches": [],
                "game_history": []
            }
            with open(self.db_path, 'w') as f:
                json.dump(initial_data, f, indent=4)
    
    def add_player_vs_ai(self, name, piece_color):
        data = self.load_data()
        player_data = {
            "id": len(data["players"]) + 1,
            "name": name,
            "mode": "vs_ai",
            "piece_color": piece_color,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        data["players"].append(player_data)
        self.save_data(data)
        return player_data["id"]
    
    def add_pvp_match(self, player1_name, player2_name, p1_piece_color, p2_piece_color):
        data = self.load_data()
        match_data = {
            "match_id": len(data["matches"]) + 1,
            "player1": player1_name,
            "player2": player2_name,
            "player1_color": p1_piece_color,
            "player2_color": p2_piece_color,
            "mode": "pvp",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        data["matches"].append(match_data)
        self.save_data(data)
        return match_data["match_id"]
    
    def get_player_data(self, player_id):
        data = self.load_data()
        for player in data["players"]:
            if player["id"] == player_id:
                return player
        return None
    
    def get_match_data(self, match_id):
        data = self.load_data()
        for match in data["matches"]:
            if match["match_id"] == match_id:
                return match
        return None
    
    def update_game_history(self, match_id, winner, moves):
        data = self.load_data()
        history_entry = {
            "match_id": match_id,
            "winner": winner,
            "moves": moves,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data["game_history"].append(history_entry)
        self.save_data(data)
    
    def load_data(self):
        with open(self.db_path, 'r') as f:
            return json.load(f)
    
    def save_data(self, data):
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=4)
