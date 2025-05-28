// src/prelude.rs
pub(crate) use bevy::prelude::*;
// 他のプロジェクト共通で使うクレートのpreludeもここに追加できます
// pub(crate) use another_crate::prelude::*;

// プロジェクト内の共通アイテム (例)
// pub(crate) use crate::common_component::CommonComponent;
// pub(crate) use crate::common_resource::CommonResource;

// 各モジュール用のprelude (例)
// pub(crate) mod audio {
//     pub(crate) use crate::audio::prelude::*;
// }