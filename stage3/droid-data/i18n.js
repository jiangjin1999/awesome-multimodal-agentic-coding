window.DROID_I18N = {
  "zh-CN": {
    "META": {
      "A": {
        "size": "678 KB",
        "file": "metadata_AUTOLab+0d4edc83+2023-10-27-20h-20m-26s.json",
        "meta": [
          [
            "lab",
            "AUTOLab",
            "哪个实验室录的"
          ],
          [
            "date",
            "2023-10-27",
            "哪天录的"
          ],
          [
            "current_task",
            "Move object into or out of container …",
            "任务。这条只写了任务类别：把物体放进或拿出容器"
          ],
          [
            "success",
            "true",
            "操作员录完按了“成功”"
          ],
          [
            "trajectory_length",
            "97",
            "一共多少拍"
          ],
          [
            "ext1 / ext2 / wrist_cam_serial",
            "22008760 / 24400334 / 18026681",
            "三台相机的编号，对应视频文件名"
          ],
          [
            "*_cam_extrinsics",
            "6 个数",
            "相机放在哪、朝哪"
          ]
        ]
      },
      "B": {
        "size": "759 KB",
        "file": "metadata_AUTOLab+84bd5053+2023-08-18-12h-06m-13s.json",
        "meta": [
          [
            "lab",
            "AUTOLab",
            "哪个实验室录的"
          ],
          [
            "date",
            "2023-08-18",
            "哪天录的"
          ],
          [
            "current_task",
            "drop yellow block into blue cup",
            "任务。这条写了具体指令：把黄方块丢进蓝杯"
          ],
          [
            "success",
            "true",
            "操作员录完按了“成功”"
          ],
          [
            "trajectory_length",
            "99",
            "一共多少拍"
          ],
          [
            "ext1 / ext2 / wrist_cam_serial",
            "22008760 / 24400334 / 18026681",
            "三台相机的编号，对应视频文件名"
          ],
          [
            "*_cam_extrinsics",
            "6 个数",
            "相机放在哪、朝哪"
          ]
        ]
      }
    },
    "TEXT": {
      "A": {
        "lead": "以第 30 拍为例：指令里手的高度是 23.8 厘米，实测还在 28.2 厘米，指令先到了 4 厘米。整条平均领先约 3.3 厘米。",
        "grip": "指令最高只到 0.78，因为手柄扳机没有按到底。实测更低，停在 0.53，因为方块卡在两根手指中间，夹不到底。所以实测停在半中间，恰好说明“手里夹着东西”。松手时指令一下掉到 0.28，实测要过 0.6 秒左右才完全张开。"
      },
      "B": {
        "lead": "以第 25 拍为例：指令里手的高度是 27.8 厘米，实测还在 34.8 厘米，指令先到了 7 厘米（这条手移动得快，领先也更多）。整条平均领先约 3.8 厘米。",
        "grip": "指令最高到 0.86，实测停在 0.61，因为黄方块卡在两根手指中间。松手时指令在第 86 拍从 0.85 掉到 0.36，实测要到第 96 拍左右才完全张开，也就是要等 0.7 秒左右。"
      }
    },
    "cases": {
      "A": {
        "phases": [
          {
            "name": "还没开始",
            "desc": "手停在原处没动。前 15 拍操作员还没按“允许移动”"
          },
          {
            "name": "伸过去、往下探",
            "desc": "手从高处斜着降到方块上方"
          },
          {
            "name": "合夹爪",
            "desc": "手几乎停住，夹爪慢慢合上"
          },
          {
            "name": "抬起、搬到碗上方",
            "desc": "夹着方块抬高，再往前送"
          },
          {
            "name": "边走边松手",
            "desc": "手还在往前走，夹爪已经张开，方块落进碗里"
          }
        ],
        "keys": [
          "开始",
          "下探途中",
          "最低点，正在合夹爪",
          "夹住了",
          "抬到最高",
          "开始松手",
          "结束"
        ]
      },
      "B": {
        "phases": [
          {
            "name": "还没开始",
            "desc": "手停在原处没动。前 13 拍操作员还没按“允许移动”"
          },
          {
            "name": "伸过去、往下探",
            "desc": "手从高处斜着降到黄方块上方"
          },
          {
            "name": "合夹爪",
            "desc": "手放慢，夹爪合上"
          },
          {
            "name": "抬起、搬到杯子上方",
            "desc": "抬得比 A 高，横向移动近 30 厘米"
          },
          {
            "name": "停住、松手",
            "desc": "手停下来再张开夹爪，和 A 不一样"
          },
          {
            "name": "结束",
            "desc": "最后 4 拍又标成了 skip_action"
          }
        ],
        "keys": [
          "开始",
          "下探途中",
          "正在合夹爪",
          "夹住了",
          "抬到最高",
          "停住松手",
          "结束"
        ]
      }
    },
    "labels": {
      "episode_id": "这条数据的编号",
      "trajectory_file": "轨迹：每一拍的数字（这一页的重点）",
      "metadata_file": "说明：实验室、任务、是否成功、相机编号",
      "camera_one": "外部相机 1 的画面",
      "camera_two": "外部相机 2 的画面（下面用的就是这一路）",
      "stereo_file": "同两台相机的双目原始录像，可以算出深度",
      "gripper": "夹爪",
      "gripper_short": "夹爪",
      "row_when": "案例 {case} 第 {step} 拍（{time} 秒，{label}）",
      "intro_length": "案例 {case} 一共 {duration} 秒，记了 {total} 拍。",
      "table_length": "案例 {case} 一共 {total} 行",
      "seconds": "秒",
      "top_view": "俯视图",
      "base_origin": "底座（原点）",
      "axis_x": "x 前",
      "axis_y": "y 左",
      "grid_scale": "格子 10 厘米",
      "start": "起点",
      "step": "第 {step} 拍",
      "total_steps": "共 {total} 拍",
      "time": "{time} 秒",
      "x_motion": "x 前后",
      "y_motion": "y 左右",
      "command": "指令",
      "measured": "实测",
      "open_zero": "0 开",
      "closed_one": "1 合",
      "image_error": "视频画面没能加载，轨迹和图表不受影响。",
      "image_loading": "画面加载中…",
      "above_frame": "手在画面上方，出画了",
      "frame_caption": "外部相机 2 · 第 {step} 拍",
      "fully_open": "全开",
      "closing": "正在合",
      "opening": "正在张开",
      "holding": "合着，手指间夹着东西",
      "mostly_open": "基本张开",
      "skip_step": "这一拍标了 skip_action：不算数",
      "position_x": "在底座前方 {value} 厘米",
      "position_left": "偏左 {value} 厘米",
      "position_right": "偏右 {value} 厘米",
      "position_z": "比底座高 {value} 厘米",
      "roll_explanation": "夹爪朝下（roll 约 ±3.14）",
      "rotation_explanation": "三个角合起来：比开头转了 {value}°",
      "play": "播放",
      "pause": "暂停",
      "data_error": "数据没能加载（{message}），交互部分暂时不可用，文字说明不受影响。"
    }
  },
  "en": {
    "META": {
      "A": {
        "size": "678 KB",
        "file": "metadata_AUTOLab+0d4edc83+2023-10-27-20h-20m-26s.json",
        "meta": [
          [
            "lab",
            "AUTOLab",
            "Lab that made the recording"
          ],
          [
            "date",
            "2023-10-27",
            "Recording date"
          ],
          [
            "current_task",
            "Move object into or out of container …",
            "Task category only: move an object into or out of a container"
          ],
          [
            "success",
            "true",
            "The operator marked success after recording"
          ],
          [
            "trajectory_length",
            "97",
            "Total number of steps"
          ],
          [
            "ext1 / ext2 / wrist_cam_serial",
            "22008760 / 24400334 / 18026681",
            "Three camera serials, matching the video filenames"
          ],
          [
            "*_cam_extrinsics",
            "6 values",
            "Camera positions and orientations"
          ]
        ]
      },
      "B": {
        "size": "759 KB",
        "file": "metadata_AUTOLab+84bd5053+2023-08-18-12h-06m-13s.json",
        "meta": [
          [
            "lab",
            "AUTOLab",
            "Lab that made the recording"
          ],
          [
            "date",
            "2023-08-18",
            "Recording date"
          ],
          [
            "current_task",
            "drop yellow block into blue cup",
            "Specific task: drop the yellow block into the blue cup"
          ],
          [
            "success",
            "true",
            "The operator marked success after recording"
          ],
          [
            "trajectory_length",
            "99",
            "Total number of steps"
          ],
          [
            "ext1 / ext2 / wrist_cam_serial",
            "22008760 / 24400334 / 18026681",
            "Three camera serials, matching the video filenames"
          ],
          [
            "*_cam_extrinsics",
            "6 values",
            "Camera positions and orientations"
          ]
        ]
      }
    },
    "TEXT": {
      "A": {
        "lead": "At step 30, for example, the commanded height is 23.8 cm, while the measured height is still 28.2 cm: the command is about 4 cm ahead on the descent. The mean positional gap across this episode is about 3.3 cm.",
        "grip": "The command peaks at only 0.78 because the controller trigger was not fully pressed. The measured value stops lower, at 0.53, because the block prevents the fingers from closing fully. Here, that intermediate value means the gripper is holding something. On release, the command drops to 0.28, but the measured gripper takes about 0.6 s to open fully."
      },
      "B": {
        "lead": "At step 25, the commanded height is 27.8 cm while the measured height is still 34.8 cm, a 7 cm lead on the descent. The hand moves faster in this episode, so the gap is larger. The mean positional gap is about 3.8 cm.",
        "grip": "The command reaches 0.86, while the measured value stops at 0.61 because the yellow block sits between the fingers. At step 86 the release command drops from 0.85 to 0.36; the measured gripper does not fully open until around step 96, roughly 0.7 s later."
      }
    },
    "cases": {
      "A": {
        "phases": [
          {
            "name": "Before motion",
            "desc": "The hand stays still. Motion is not enabled during the first 15 steps"
          },
          {
            "name": "Reach and lower",
            "desc": "The hand descends diagonally toward the block"
          },
          {
            "name": "Close gripper",
            "desc": "The hand nearly stops as the gripper closes slowly"
          },
          {
            "name": "Lift and carry to bowl",
            "desc": "The hand lifts the block, then carries it forward"
          },
          {
            "name": "Release while moving",
            "desc": "The gripper opens while the hand still moves forward, dropping the block into the bowl"
          }
        ],
        "keys": [
          "Start",
          "Lowering",
          "Lowest point, gripper closing",
          "Block grasped",
          "Highest point",
          "Release begins",
          "End"
        ]
      },
      "B": {
        "phases": [
          {
            "name": "Before motion",
            "desc": "The hand stays still. Motion is not enabled during the first 13 steps"
          },
          {
            "name": "Reach and lower",
            "desc": "The hand descends diagonally toward the yellow block"
          },
          {
            "name": "Close gripper",
            "desc": "The hand slows down and the gripper closes"
          },
          {
            "name": "Lift and carry to cup",
            "desc": "The hand lifts higher than in A and moves nearly 30 cm sideways"
          },
          {
            "name": "Stop and release",
            "desc": "Unlike A, the hand stops before the gripper opens"
          },
          {
            "name": "End",
            "desc": "The last 4 steps are marked skip_action again"
          }
        ],
        "keys": [
          "Start",
          "Lowering",
          "Gripper closing",
          "Block grasped",
          "Highest point",
          "Stopped, releasing",
          "End"
        ]
      }
    },
    "labels": {
      "episode_id": "Episode ID",
      "trajectory_file": "Trajectory: numbers for every step (the focus of this page)",
      "metadata_file": "Metadata: lab, task, success, and camera serials",
      "camera_one": "External camera 1 video",
      "camera_two": "External camera 2 video (used below)",
      "stereo_file": "Raw stereo recordings from both cameras; usable for depth reconstruction",
      "gripper": "Gripper",
      "gripper_short": "Grip",
      "row_when": "case {case}, step {step} ({time} s, {label})",
      "intro_length": "Case {case} lasts {duration} seconds and contains {total} steps.",
      "table_length": "case {case} has {total} rows",
      "seconds": "s",
      "top_view": "Top view",
      "base_origin": "Base (origin)",
      "axis_x": "x forward",
      "axis_y": "y left",
      "grid_scale": "10 cm grid",
      "start": "Start",
      "step": "Step {step}",
      "total_steps": "of {total} steps",
      "time": "{time} s",
      "x_motion": "x forward/back",
      "y_motion": "y left/right",
      "command": "Command",
      "measured": "Measured",
      "open_zero": "0 open",
      "closed_one": "1 closed",
      "image_error": "Camera frames could not load. The trajectory and charts still work.",
      "image_loading": "Loading camera frame…",
      "above_frame": "The hand is above the camera frame",
      "frame_caption": "External camera 2 · Step {step}",
      "fully_open": "Fully open",
      "closing": "Closing",
      "opening": "Opening",
      "holding": "Closed around an object",
      "mostly_open": "Mostly open",
      "skip_step": "This step is marked skip_action: exclude its action",
      "position_x": "{value} cm forward of the base",
      "position_left": "{value} cm to the left",
      "position_right": "{value} cm to the right",
      "position_z": "{value} cm above the base",
      "roll_explanation": "Gripper points down (roll ≈ ±3.14)",
      "rotation_explanation": "Combined rotation: {value}° from the start",
      "play": "Play",
      "pause": "Pause",
      "data_error": "Data could not load ({message}). Interactive controls are unavailable; the written explanation remains readable."
    }
  },
  "ja": {
    "META": {
      "A": {
        "size": "678 KB",
        "file": "metadata_AUTOLab+0d4edc83+2023-10-27-20h-20m-26s.json",
        "meta": [
          [
            "lab",
            "AUTOLab",
            "記録した研究室"
          ],
          [
            "date",
            "2023-10-27",
            "記録日"
          ],
          [
            "current_task",
            "Move object into or out of container …",
            "タスクのカテゴリのみ：物体を容器に入れる／取り出す"
          ],
          [
            "success",
            "true",
            "記録後に操作者が「成功」を押した"
          ],
          [
            "trajectory_length",
            "97",
            "総ステップ数"
          ],
          [
            "ext1 / ext2 / wrist_cam_serial",
            "22008760 / 24400334 / 18026681",
            "3 台のカメラ番号。動画のファイル名に対応"
          ],
          [
            "*_cam_extrinsics",
            "6 つの数値",
            "カメラの位置と姿勢"
          ]
        ]
      },
      "B": {
        "size": "759 KB",
        "file": "metadata_AUTOLab+84bd5053+2023-08-18-12h-06m-13s.json",
        "meta": [
          [
            "lab",
            "AUTOLab",
            "記録した研究室"
          ],
          [
            "date",
            "2023-08-18",
            "記録日"
          ],
          [
            "current_task",
            "drop yellow block into blue cup",
            "具体的なタスク：黄色いブロックを青いカップに落とす"
          ],
          [
            "success",
            "true",
            "記録後に操作者が「成功」を押した"
          ],
          [
            "trajectory_length",
            "99",
            "総ステップ数"
          ],
          [
            "ext1 / ext2 / wrist_cam_serial",
            "22008760 / 24400334 / 18026681",
            "3 台のカメラ番号。動画のファイル名に対応"
          ],
          [
            "*_cam_extrinsics",
            "6 つの数値",
            "カメラの位置と姿勢"
          ]
        ]
      }
    },
    "TEXT": {
      "A": {
        "lead": "たとえばステップ 30 では、高さの指令値は 23.8 cm ですが、実測値はまだ 28.2 cm です。下降する方向に、指令が約 4 cm 先行しています。全体での位置の差は平均約 3.3 cm です。",
        "grip": "コントローラーのトリガーを最後まで押していないため、指令値の最大は 0.78 です。実測値はさらに低い 0.53 で止まります。指の間にブロックがあり、最後まで閉じられないためです。この中間の値は、物体をつかんでいることを示しています。放すときは指令値が 0.28 まで下がりますが、実際に全開になるまでには約 0.6 秒かかります。"
      },
      "B": {
        "lead": "ステップ 25 では、高さの指令値が 27.8 cm なのに対し、実測値はまだ 34.8 cm で、下降方向に 7 cm の差があります。この例は手の動きが速いため、先行する幅も大きくなっています。全体での位置の差は平均約 3.8 cm です。",
        "grip": "指令値は最大 0.86 ですが、黄色いブロックが指の間にあるため、実測値は 0.61 で止まります。ステップ 86 で放す指令が 0.85 から 0.36 に下がり、実際に全開になるのはステップ 96 付近です。約 0.7 秒の遅れがあります。"
      }
    },
    "cases": {
      "A": {
        "phases": [
          {
            "name": "動作開始前",
            "desc": "手は停止している。最初の 15 ステップは移動が許可されていない"
          },
          {
            "name": "近づけて下ろす",
            "desc": "手を斜めに下ろし、ブロックの上へ近づける"
          },
          {
            "name": "グリッパーを閉じる",
            "desc": "手がほぼ止まり、グリッパーがゆっくり閉じる"
          },
          {
            "name": "持ち上げてボウルへ",
            "desc": "ブロックをつかんで持ち上げ、前方へ運ぶ"
          },
          {
            "name": "動かしながら放す",
            "desc": "前進しながらグリッパーを開き、ブロックがボウルに落ちる"
          }
        ],
        "keys": [
          "開始",
          "下降中",
          "最も低い位置でグリッパーを閉じている",
          "ブロックをつかんだ",
          "最も高い位置",
          "放し始める",
          "終了"
        ]
      },
      "B": {
        "phases": [
          {
            "name": "動作開始前",
            "desc": "手は停止している。最初の 13 ステップは移動が許可されていない"
          },
          {
            "name": "近づけて下ろす",
            "desc": "手を斜めに下ろし、黄色いブロックの上へ近づける"
          },
          {
            "name": "グリッパーを閉じる",
            "desc": "手の動きが遅くなり、グリッパーが閉じる"
          },
          {
            "name": "持ち上げてカップへ",
            "desc": "例 A より高く持ち上げ、横方向に約 30 cm 動かす"
          },
          {
            "name": "止めて放す",
            "desc": "例 A と違い、手を止めてからグリッパーを開く"
          },
          {
            "name": "終了",
            "desc": "最後の 4 ステップは再び skip_action になる"
          }
        ],
        "keys": [
          "開始",
          "下降中",
          "グリッパーを閉じている",
          "ブロックをつかんだ",
          "最も高い位置",
          "停止して放す",
          "終了"
        ]
      }
    },
    "labels": {
      "episode_id": "このデータの ID",
      "trajectory_file": "軌跡：各ステップの数値（このページの中心）",
      "metadata_file": "メタデータ：研究室、作業、成否、カメラ番号",
      "camera_one": "外部カメラ 1 の映像",
      "camera_two": "外部カメラ 2 の映像（以下で使用）",
      "stereo_file": "同じ 2 台のステレオカメラの元映像。深度を計算できる",
      "gripper": "グリッパー",
      "gripper_short": "開閉",
      "row_when": "例 {case} のステップ {step}（{time} 秒、{label}）",
      "intro_length": "例 {case} は {duration} 秒間、全 {total} ステップの記録です。",
      "table_length": "例 {case} は全 {total} 行です",
      "seconds": "秒",
      "top_view": "俯瞰図",
      "base_origin": "台座（原点）",
      "axis_x": "x 前方",
      "axis_y": "y 左方",
      "grid_scale": "1 マス 10 cm",
      "start": "始点",
      "step": "ステップ {step}",
      "total_steps": "全 {total} ステップ",
      "time": "{time} 秒",
      "x_motion": "x 前後",
      "y_motion": "y 左右",
      "command": "指令",
      "measured": "実測",
      "open_zero": "0 開",
      "closed_one": "1 閉",
      "image_error": "カメラ映像を読み込めませんでした。軌跡とグラフは引き続き利用できます。",
      "image_loading": "映像を読み込み中…",
      "above_frame": "手が画面の上側にはみ出しています",
      "frame_caption": "外部カメラ 2 · ステップ {step}",
      "fully_open": "全開",
      "closing": "閉じている途中",
      "opening": "開いている途中",
      "holding": "物体を挟んでいる",
      "mostly_open": "ほぼ開いている",
      "skip_step": "このステップは skip_action：動作を除外",
      "position_x": "台座から前方に {value} cm",
      "position_left": "左に {value} cm",
      "position_right": "右に {value} cm",
      "position_z": "台座より {value} cm 上",
      "roll_explanation": "グリッパーは下向き（roll ≈ ±3.14）",
      "rotation_explanation": "3 つの角度を合わせた変化：開始時から {value}°",
      "play": "再生",
      "pause": "一時停止",
      "data_error": "データを読み込めませんでした（{message}）。操作機能は利用できませんが、本文は引き続き読めます。"
    }
  }
};
