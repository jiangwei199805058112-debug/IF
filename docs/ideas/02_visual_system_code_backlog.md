# 画面系统底层待办

> 状态：未来实现待办。当前 `v0.1` 仍不开始正式 UI，不迁移引擎。本文用于提前记录哪些内容需要在代码层面和游戏底层预留，方便后续分阶段加入。

## 1. 目标

未来画面系统不是单纯贴背景图，而是由玩家身份、场景、时间、天气、物品、关系状态和设备状态共同驱动。

底层需要支持：

- 学生/成年人不同生活阶段。
- 书本、电脑、手机、车载屏幕等场景内信息载体。
- 手机震动、亮屏、通知、聊天和定位。
- 桌面物品购买、升级、摆放和整洁度。
- 关系物品对承诺提醒、暧昧风险和对象安全感的轻微影响。
- 月份/季节驱动的随机天气。
- 1080p、2K、4K 的未来画面适配。

## 2. 数据层需要新增的结构

### 2.1 PlayerLifeProfile

用于描述玩家生活阶段和经济基础。

建议字段：

```text
identity_stage: student | adult
income_source: allowance | part_time | salary | freelance | mixed
monthly_income
monthly_fixed_cost
monthly_free_budget
residence_type
work_or_school_type
commute_type
has_vehicle
has_private_room
has_computer
has_phone_stand
```

学生模式重点：

- 零花钱。
- 兼职。
- 课程。
- 作业。
- 考试。
- 简单购物。

成年人模式重点：

- 工资。
- 房租。
- 车贷。
- 保险。
- 油费。
- 工作任务。
- 网购。
- 约会预算。

### 2.2 SceneAnchor

用于标记当前画面锚点。

建议枚举：

```text
student_desk
home_desk
office_desk
cafe_table
restaurant_table
car_driver_view
bedroom
living_room
school_classroom
library_desk
street
subway
```

建议字段：

```text
scene_id
scene_category
identity_stage_supported
time_slots_supported
required_conditions
primary_info_surface
primary_action_device
visible_object_slots
weather_visible
privacy_risk_level
```

### 2.3 DiegeticInfoSurface

用于描述“信息显示在什么现实物件上”。

建议类型：

```text
book
notebook
computer_screen
phone_screen
car_center_screen
paper_note
calendar
```

建议字段：

```text
surface_id
surface_type
summary_fields
detail_fields
can_zoom
can_show_tasks
can_show_money
can_show_weather
can_show_chat
can_show_shop
```

### 2.4 PhoneState

用于描述手机在场景中的状态。

建议字段：

```text
phone_location
is_visible
is_zoomed
screen_on
is_vibrating
has_unread_notification
notification_preview_visible
is_muted
hidden_notification_enabled
on_stand
stand_type
charging_state
```

可选状态：

```text
idle
screen_on
vibrating
calling
muted
hidden_notice
zoomed
in_chat_app
```

### 2.5 ChatAppState

用于虚构聊天软件。

建议字段：

```text
app_name
contacts
pinned_contacts
unread_counts
current_thread_id
available_reply_actions
can_send_location
can_request_location
can_call
privacy_risk_tags
```

聊天行为标签：

```text
truthful_reply
half_truth
lie
avoidance
silence
apology
explain
counter_question
send_location
request_location
hide_notification
```

### 2.6 InventoryItem / DeskItem

用于桌面物品、文具、外设、礼物、装饰、车内设备。

建议字段：

```text
item_id
display_name
category
tier
price
owner
source
is_gift
from_character_id
is_relationship_anchor
movable
interactable
upgrade_path
appearance_key
quality_score
comfort_delta
mood_delta
productivity_delta
relationship_anchor_delta
risk_modifier_delta
```

物品分类：

```text
stationery
computer_peripheral
decoration
plant
food
phone_accessory
gift
photo
vehicle_accessory
clothing
```

物品等级：

```text
cheap
normal
premium
flagship
limited
gift
memorial
```

### 2.7 DesktopLayout

用于保存玩家布置。

建议不要保存绝对像素，而保存比例坐标。

```text
scene_id
item_id
x_ratio
y_ratio
scale
rotation
z_index
locked
visible
```

### 2.8 CleanlinessState

用于桌面整洁和垃圾。

建议字段：

```text
scene_id
cleanliness
clutter
trash_count
blocked_items
last_cleaned_day
stress_contribution
visitor_impression_modifier
```

### 2.9 WeatherState

用于游戏内随机天气。

建议字段：

```text
month
season
region_profile
weather_type
temperature_band
rain_intensity
snow_intensity
umbrella_needed
commute_delay_risk
care_message_opportunity
```

天气类型：

```text
sunny
cloudy
light_rain
heavy_rain
snow
heat
cold
fog
```

### 2.10 RelationshipAnchorState

用于对象相关物品对关系的轻微影响。

建议字段：

```text
character_id
anchor_item_count
anchor_strength
visible_to_partner
player_side_anchor_strength
partner_side_anchor_strength
commitment_reminder_delta
affair_risk_soft_modifier
reassurance_delta
```

限制：

- 该系统只做小幅修正。
- 不得覆盖人格、信任、满意度、冲突记忆和长期行为模式。

## 3. 逻辑层需要新增的服务

### 3.1 SceneSelectionService

根据玩家身份、时间、地点、事件和资产状态选择场景。

输入：

```text
PlayerLifeProfile
current_day
current_time_slot
relationship_stage
scheduled_event
weather
location
```

输出：

```text
SceneAnchor
visible_objects
primary_info_surface
primary_action_device
```

### 3.2 DiegeticInfoComposer

把游戏状态转换成书本/电脑/手机上可以显示的摘要。

职责：

- 学生模式生成书本摘要。
- 成年人模式生成电脑摘要。
- 手机生成通知、聊天列表和选择项。
- 控制摘要信息数量，避免画面内文字过小。

### 3.3 PhoneInteractionService

处理手机点击、放大、通知、震动、隐藏通知和聊天选择。

职责：

- 生成手机状态。
- 处理未读消息。
- 处理发定位/请求定位。
- 处理静音和隐藏通知。
- 处理对象查手机风险。

### 3.4 SeasonalWeatherGenerator

根据月份、季节和地区生成随机天气。

职责：

- 保证天气符合大致季节规律。
- 给约会、通勤、关心话语提供钩子。
- 不依赖真实天气 API。

### 3.5 ShopCatalogService

处理商店、物品价格、等级和购买。

职责：

- 学生商店和成年人商店分开。
- 按收入、零花钱和生活阶段控制可买物品。
- 支持桌面物品、礼物、衣服、手机支架、车内设备等。

### 3.6 DesktopLayoutService

处理建造模式和摆放保存。

职责：

- 保存比例坐标。
- 读取布局。
- 控制哪些物品可移动。
- 防止核心信息载体被移动到不可用位置。

### 3.7 CleanlinessService

处理桌面变乱、垃圾生成和清理。

职责：

- 根据时间、压力、生活习惯生成垃圾。
- 长期不清理时降低整洁度。
- 对学习/工作效率、对象来访印象、操作遮挡产生影响。

### 3.8 RelationshipAnchorModifier

处理合影、礼物、情侣物品等关系锚点的轻微修正。

职责：

- 根据双方桌面是否摆放关系物品计算承诺提醒。
- 对暧昧/出轨/隐瞒风险做小幅修正。
- 不允许该修正压过核心关系系统。

## 4. 事件系统需要扩展的字段

未来事件卡可以新增以下字段。

```text
scene_anchor
required_info_surface
primary_action_device
visible_objects
phone_notification_hook
computer_summary_hook
book_summary_hook
weather_hook
shop_hook
layout_hook
cleanliness_hook
relationship_anchor_hook
privacy_risk_tags
```

示例：

```text
scene_anchor: office_desk
primary_action_device: phone
required_info_surface: computer_screen
visible_objects: [computer, phone, coffee, keyboard]
phone_notification_hook: partner_message
weather_hook: heavy_rain_care_prompt
privacy_risk_tags: [coworker_nearby, computer_chat_visible]
```

## 5. 表现层未来需要的能力

该部分只记录未来 UI/引擎需要，不代表当前马上实现。

需要支持：

- 2D 第一人称生活场景。
- 分层背景、固定物品、可移动物品、效果层、设备 UI 层。
- 手机震动、亮屏、闪动。
- 点击手机后平滑放大。
- 点击电脑/书本后平滑放大。
- 建造模式拖动物品。
- 物品层级、缩放、旋转。
- 1080p、2K、4K 响应式适配。
- 车内驾驶座第一人称视角。

建议表现层结构：

```text
SceneRoot
├── BackgroundLayer
├── FixedObjectLayer
├── MovableObjectLayer
├── InteractiveHotspotLayer
├── EffectLayer
├── DeviceUILayer
└── SystemUILayer
```

## 6. 分阶段落地建议

### 阶段 0：当前文档记录

只记录创意和底层待办，不写正式 UI。

### 阶段 1：纯数据结构草案

可以先新增 JSON/schema 文档，不接画面。

产物：

- 场景锚点枚举。
- 信息载体枚举。
- 手机状态结构。
- 物品等级和桌面物品 schema。
- 天气权重表草案。

### 阶段 2：控制台文本原型

在控制台中模拟“书本/电脑/手机”的输出。

示例：

```text
【学生课桌｜书本摘要】
零花钱：120
今日课程：数学、英语
天气：小雨，适合提醒对方带伞

【手机】
对象发来消息：你今天放学几点？
1. 真实回答
2. 晚点再回
3. 发定位
```

### 阶段 3：灰盒 UI 原型

未来如果开始做画面，优先做一个灰盒原型。

最小目标：

- 桌面直接显示。
- 手机在右侧。
- 书本/电脑显示摘要。
- 点击手机放大。
- 聊天列表和简单回复。

### 阶段 4：桌面建造与商店

加入购买、摆放、保存布局、桌面垃圾和关系锚点。

### 阶段 5：场景扩展

加入办公桌、车内驾驶座、咖啡厅、同居房间等。

## 7. 测试建议

如果未来写代码，需要最少覆盖：

- 学生/成年人信息载体选择是否正确。
- 不同月份天气权重是否合理。
- 物品购买是否受预算限制。
- 桌面布局保存是否使用比例坐标。
- 关系锚点只产生小幅修正。
- 隐私风险不会因为隐藏通知完全消失。
- 手机/电脑/书本摘要不暴露玩家本不应知道的真实数值。
- 无 UI 环境下控制台流程仍能运行。

## 8. 当前非目标

当前不做：

- 正式 UI。
- 正式美术。
- 引擎迁移。
- AI 图像生成接入。
- 真实品牌物品。
- 真实天气 API。
- 复杂 3D 驾驶系统。
- 完整桌面建造模式。

后续任何实现都必须继续遵守项目现有边界：先保证关系系统、事件系统和 14 天闭环稳定，再逐步接生活行动层和视觉表现层。