// src/main.rs
use bevy::prelude::*;
use bevy::core_pipeline::core_2d::Camera2dBundle;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2dBundle::default());
}