import arcade
import os


# =========================================================
# KONSTANTA
# =========================================================

TILE_SCALING = 1

TILE_SIZE = 18

SCREEN_WIDTH = 50 * TILE_SIZE
SCREEN_HEIGHT = 45 * TILE_SIZE

SCREEN_TITLE = "Dunia Permen"

PLAYER_MOVEMENT_SPEED = 2

GRAVITY = 0.5

JUMP_SPEED = 15

STARTING_LIVES = 3

POINTS_PER_ITEM = 10

# Jarak tambahan untuk mendeteksi obstacle
DAMAGE_MARGIN = 8


# =========================================================
# LEVEL
# =========================================================

STARTING_LEVEL = 1


# =========================================================
# KEY CONFIGURATION
# =========================================================

# GID Key dari Tiled
KEY_GID = 28


# =========================================================
# GAME
# =========================================================

class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(
            width,
            height,
            title,
            resizable=False
        )

        # =================================================
        # LEVEL
        # =================================================

        self.current_level = STARTING_LEVEL

        # =================================================
        # TILEMAP
        # =================================================

        self.tile_map = None

        # =================================================
        # SPRITE LIST
        # =================================================

        self.background2 = arcade.SpriteList()

        self.background = arcade.SpriteList()

        self.ground = arcade.SpriteList()

        self.props = arcade.SpriteList()

        self.obstacles = arcade.SpriteList()

        self.players = arcade.SpriteList()

        # =================================================
        # PLAYER
        # =================================================

        self.player = None

        self.spawn_x = 0

        self.spawn_y = 0

        # =================================================
        # COLLISION
        # =================================================

        self.walls = arcade.SpriteList()

        self.physics_engine = None

        # =================================================
        # KEYBOARD
        # =================================================

        self.left_pressed = False

        self.right_pressed = False

        # =================================================
        # GAME DATA
        # =================================================

        self.score = 0

        self.lives = STARTING_LIVES

        self.game_over = False

        self.game_finished = False

        # =================================================
        # KEY DATA
        # =================================================

        self.total_keys = 0

        self.keys_collected = 0

        # =================================================
        # OBSTACLE DAMAGE CONTROL
        # =================================================

        self.can_take_damage = True

        self.damage_cooldown = 0


    # =====================================================
    # SETUP
    # =====================================================

    def setup(self):

        self.current_level = STARTING_LEVEL

        self.score = 0

        self.lives = STARTING_LIVES

        self.game_over = False

        self.game_finished = False

        self.left_pressed = False

        self.right_pressed = False

        self.load_level(self.current_level)


    # =====================================================
    # LOAD LEVEL
    # =====================================================

    def load_level(self, level_number):

        print()
        print("========================================")
        print(f"LOAD LEVEL {level_number}")
        print("========================================")

        # -------------------------------------------------
        # RESET LEVEL DATA
        # -------------------------------------------------

        self.game_over = False

        self.game_finished = False

        self.keys_collected = 0

        self.can_take_damage = True

        self.damage_cooldown = 0

        # -------------------------------------------------
        # LEVEL FILE
        # -------------------------------------------------

        level_file = f"level{level_number}.json"

        # -------------------------------------------------
        # CHECK FILE
        # -------------------------------------------------

        if not os.path.exists(level_file):

            print(
                f"File {level_file} tidak ditemukan."
            )

            print(
                "Game selesai."
            )

            self.game_finished = True

            return

        # -------------------------------------------------
        # LOAD TILEMAP
        # -------------------------------------------------

        self.tile_map = arcade.load_tilemap(
            level_file,
            scaling=TILE_SCALING
        )

        # =================================================
        # LOAD LAYERS
        # =================================================

        self.background = self.get_layer(
            "background"
        )

        self.ground = self.get_layer(
            "ground"
        )

        self.obstacles = self.get_layer(
            "obstacles"
        )

        self.props = self.get_layer(
            "props"
        )

        self.players = self.get_layer(
            "players"
        )

        # =================================================
        # PLAYER
        # =================================================

        if len(self.players) == 0:

            print(
                "ERROR: Tidak ada player "
                "pada layer 'players'."
            )

            self.game_finished = True

            return

        self.player = self.players[0]

        # -------------------------------------------------
        # SIMPAN SPAWN
        # -------------------------------------------------

        self.spawn_x = self.player.center_x

        self.spawn_y = self.player.center_y

        # =================================================
        # CREATE WALLS
        # =================================================

        self.create_walls()

        # =================================================
        # COUNT KEYS
        # =================================================

        self.count_keys()

        # =================================================
        # PHYSICS
        # =================================================

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.walls,
            gravity_constant=GRAVITY
        )

        print(
            f"Player spawn: "
            f"{self.spawn_x}, {self.spawn_y}"
        )

        print(
            f"Obstacle: {len(self.obstacles)}"
        )

        print(
            f"Props: {len(self.props)}"
        )

        print(
            f"Keys: {self.total_keys}"
        )

        print(
            f"Total collision objects: "
            f"{len(self.walls)}"
        )


    # =====================================================
    # GET LAYER
    # =====================================================

    def get_layer(self, layer_name):

        if layer_name in self.tile_map.sprite_lists:

            return self.tile_map.sprite_lists[
                layer_name
            ]

        return arcade.SpriteList()


    # =====================================================
    # CREATE WALLS
    # =====================================================

    def create_walls(self):

        self.walls = arcade.SpriteList()

        # -------------------------------------------------
        # GROUND
        # -------------------------------------------------

        for sprite in self.ground:

            self.walls.append(sprite)

        # -------------------------------------------------
        # OBSTACLES
        # -------------------------------------------------

        for sprite in self.obstacles:

            self.walls.append(sprite)


    # =====================================================
    # COUNT KEY
    # =====================================================

    def count_keys(self):

        self.total_keys = 0

        for prop in self.props:

            if self.is_key(prop):

                self.total_keys += 1

        print(
            f"Total key pada level: "
            f"{self.total_keys}"
        )


    # =====================================================
    # CHECK KEY BY GID
    # =====================================================

    def is_key(self, sprite):

        try:

            # Ambil GID dari properties sprite
            gid = sprite.properties.get("gid")

            return gid == KEY_GID

        except AttributeError:

            return False


    # =====================================================
    # DRAW
    # =====================================================

    def on_draw(self):

        self.clear()

        # =================================================
        # MAP
        # =================================================

        self.background.draw()

        self.ground.draw()

        self.obstacles.draw()

        self.props.draw()

        self.players.draw()

        # =================================================
        # LEVEL
        # =================================================

        arcade.draw_text(
            f"Level: {self.current_level}",
            20,
            SCREEN_HEIGHT - 35,
            arcade.color.WHITE,
            12
        )

        # =================================================
        # SCORE
        # =================================================

        arcade.draw_text(
            f"Score: {self.score}",
            60,
            SCREEN_HEIGHT - 35,
            arcade.color.WHITE,
            12
        )

        # =================================================
        # LIVES
        # =================================================

        arcade.draw_text(
            f"Lives: {self.lives}",
            110,
            SCREEN_HEIGHT - 35,
            arcade.color.WHITE,
            12
        )

        # =================================================
        # KEYS
        # =================================================

        arcade.draw_text(
            f"Keys: {self.keys_collected}/"
            f"{self.total_keys}",
            160,
            SCREEN_HEIGHT - 35,
            arcade.color.WHITE,
            12
        )

        # =================================================
        # GAME OVER
        # =================================================

        if self.game_over:

            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.RED,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                "Press R to Restart",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 50,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

        # =================================================
        # GAME FINISHED
        # =================================================

        if self.game_finished:

            arcade.draw_text(
                "YOU WIN!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.YELLOW,
                45,
                anchor_x="center"
            )


    # =====================================================
    # UPDATE
    # =====================================================

    def on_update(self, delta_time):

        # =================================================
        # GAME STOP
        # =================================================

        if self.game_over:

            return

        if self.game_finished:

            return

        # =================================================
        # DAMAGE COOLDOWN
        # =================================================

        if self.damage_cooldown > 0:

            self.damage_cooldown -= delta_time

            if self.damage_cooldown <= 0:

                self.can_take_damage = True

        # =================================================
        # MOVEMENT
        # =================================================

        self.player.change_x = 0

        if self.left_pressed:

            self.player.change_x = -PLAYER_MOVEMENT_SPEED
            

        if self.right_pressed:

            self.player.change_x = PLAYER_MOVEMENT_SPEED

        # =================================================
        # PHYSICS
        # =================================================

        self.physics_engine.update()
        # =================================================
        # SCREEN BOUNDARY
        # =================================================

        if self.player.left < 0:

            self.player.left = 0
            self.player.change_x = 0


        if self.player.right > SCREEN_WIDTH:

            self.player.right = SCREEN_WIDTH
            self.player.change_x = 0

        # =================================================
        # OBSTACLE DAMAGE
        # =================================================

        self.check_obstacle_collision()

        # =================================================
        # KEY / PROP COLLISION
        # =================================================

        self.collect_props()

    # =====================================================
    # COLLECT PROPS
    # =====================================================

    def collect_props(self):

        hit_props = arcade.check_for_collision_with_list(
            self.player,
            self.props
        )

        for prop in hit_props:

            # -------------------------------------------------
            # KEY
            # -------------------------------------------------

            if self.is_key(prop):

                self.keys_collected += 1

                self.score += POINTS_PER_ITEM

                print(
                    f"KEY: "
                    f"{self.keys_collected}/"
                    f"{self.total_keys}"
                )

                prop.remove_from_sprite_lists()

                # -------------------------------------------------
                # SEMUA KEY TERKUMPUL
                # -------------------------------------------------

                if (
                    self.total_keys > 0
                    and self.keys_collected
                    >= self.total_keys
                ):

                    self.complete_level()

            # -------------------------------------------------
            # PROP BIASA
            # -------------------------------------------------

            else:

                self.score += POINTS_PER_ITEM

                prop.remove_from_sprite_lists()



    # =====================================================
    # OBSTACLE COLLISION
    # =====================================================

    def check_obstacle_collision(self):

        # =================================================
        # COOLDOWN
        # =================================================

        if not self.can_take_damage:

            return

        # =================================================
        # CHECK SETIAP OBSTACLE
        # =================================================

        for obstacle in self.obstacles:

            # -------------------------------------------------
            # PERBESAR AREA DAMAGE
            # -------------------------------------------------

            obstacle_left = (
                obstacle.left - DAMAGE_MARGIN
            )

            obstacle_right = (
                obstacle.right + DAMAGE_MARGIN
            )

            obstacle_bottom = (
                obstacle.bottom - DAMAGE_MARGIN
            )

            obstacle_top = (
                obstacle.top + DAMAGE_MARGIN
            )

            # -------------------------------------------------
            # CHECK PLAYER
            # -------------------------------------------------

            if (
                self.player.right > obstacle_left
                and self.player.left < obstacle_right
                and self.player.top > obstacle_bottom
                and self.player.bottom < obstacle_top
            ):

                print(
                    "PLAYER MENYENTUH OBSTACLE!"
                )

                # =================================================
                # KURANGI NYAWA
                # =================================================

                self.lives -= 1

                print(
                    f"Nyawa tersisa: {self.lives}"
                )

                # =================================================
                # DAMAGE COOLDOWN
                # =================================================

                self.can_take_damage = False

                self.damage_cooldown = 0.5

                # =================================================
                # RESPAWN
                # =================================================

                self.respawn_player()

                # =================================================
                # GAME OVER
                # =================================================

                if self.lives <= 0:

                    self.game_over = True

                    self.player.change_x = 0

                    self.player.change_y = 0

                    print(
                        "GAME OVER"
                    )

                # Hanya satu obstacle yang memberikan damage
                return


    # =====================================================
    # RESPAWN PLAYER
    # =====================================================

    def respawn_player(self):

        self.player.center_x = self.spawn_x

        self.player.center_y = self.spawn_y

        self.player.change_x = 0

        self.player.change_y = 0

        print(
            "Player respawn."
        )


    # =====================================================
    # COMPLETE LEVEL
    # =====================================================

    def complete_level(self):

        print()

        print("========================================")

        print(
            f"LEVEL {self.current_level} SELESAI!"
        )

        print("========================================")

        # -------------------------------------------------
        # LEVEL BERIKUTNYA
        # -------------------------------------------------

        next_level = self.current_level + 1

        next_level_file = (
            f"Level{next_level}.json"
        )

        # -------------------------------------------------
        # ADA LEVEL BERIKUTNYA
        # -------------------------------------------------

        if os.path.exists(next_level_file):

            self.current_level = next_level

            print(
                f"Loading Level "
                f"{self.current_level}"
            )

            self.load_level(
                self.current_level
            )

        # -------------------------------------------------
        # SEMUA LEVEL SELESAI
        # -------------------------------------------------

        else:

            self.game_finished = True

            print()

            print("========================================")

            print(
                "SEMUA LEVEL SELESAI!"
            )

            print(
                "YOU WIN!"
            )

            print("========================================")


    # =====================================================
    # KEY PRESS
    # =====================================================

    def on_key_press(self, key, modifiers):

        # =================================================
        # RESTART
        # =================================================

        if key == arcade.key.R:

            if self.game_over:

                self.setup()

            return

        # =================================================
        # STOP INPUT
        # =================================================

        if self.game_over:

            return

        if self.game_finished:

            return

        # =================================================
        # LEFT
        # =================================================

        if (
            key == arcade.key.LEFT
            or key == arcade.key.A
        ):

            self.left_pressed = True

        # =================================================
        # RIGHT
        # =================================================

        elif (
            key == arcade.key.RIGHT
            or key == arcade.key.D
        ):

            self.right_pressed = True

        # =================================================
        # JUMP
        # =================================================

        elif (
            key == arcade.key.UP
            or key == arcade.key.W
        ):

            if self.physics_engine.can_jump():

                self.player.change_y = JUMP_SPEED


    # =====================================================
    # KEY RELEASE
    # =====================================================

    def on_key_release(self, key, modifiers):

        # =================================================
        # LEFT
        # =================================================

        if (
            key == arcade.key.LEFT
            or key == arcade.key.A
        ):

            self.left_pressed = False

        # =================================================
        # RIGHT
        # =================================================

        elif (
            key == arcade.key.RIGHT
            or key == arcade.key.D
        ):

            self.right_pressed = False


# =========================================================
# MAIN PROGRAM
# =========================================================

window = MyGame(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE
)

window.setup()

arcade.run()


        
