import streamlit as st
from io import BytesIO
from PIL import Image
from streamlit_latex_render import latex_render
from streamlit_image_label import image_label
import pandas as pd
import base64

def image_path2base64_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # 构造 data:image/png;base64, 格式
        img_data_uri = f"data:image/png;base64,{img_base64}"
    return img_data_uri

# def rotation(is_90):
#     st.session_state.current_row = st.session_state.current_row.copy()
#     image_base64 = st.session_state.current_row['image'].replace("data:image/png;base64,", "")
#     byte_data = base64.b64decode(image_base64)
#     img = Image.open(BytesIO(byte_data)).convert("RGB")
#     # 顺时针旋转90度
#     if is_90:
#         rotated_img = img.rotate(-90, expand=True)  # -90度是顺时针旋转
#     else:
#         rotated_img = img.rotate(90, expand=True)  # -90度是顺时针旋转
#     # 保存旋转后的图片到 BytesIO 对象中
#     buffered = BytesIO()
#     rotated_img.save(buffered, format="JPEG")
#     # 获取图片的 base64 编码
#     img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
#     # 构造 data:image/png;base64, 格式
#     img_data_uri = f"data:image/png;base64,{img_base64}"
#     # print(img_data_uri)
#     st.session_state.current_row['image'] = img_data_uri

st.set_page_config(
    page_title="公式批注渲染",  # 设置页面标题
    page_icon="🔍",  # 设置页面图标
    layout="wide",  # 可以选择"centered" 或 "wide"
    menu_items={
        'About': "xizhi"
    }
)


@st.dialog("登陆")
def show_verify():
    user_id = st.text_input("输入你的名字，并回车")
    if user_id in ["lixumin"]:
        st.session_state.user_id = user_id
        if st.button("登陆成功，确认"):
            st.rerun()
    else:
        st.text("输入有误或者没有给你安排任务，联系负责人")

@st.dialog("完成状态")
def done():
    st.text("已完成所有任务")
    # if st.button("确认"):
    #     st.rerun()

# if 'user_id' not in st.session_state:
#     show_verify()

if 'user_id' not in st.session_state:
        st.session_state.user_id = "lixumin"
if False:
    pass

else:
    if 'data_df' not in st.session_state:
        st.session_state.data_df = pd.DataFrame(
            [[str(i), False, [image_path2base64_image("/Users/lixumin/Desktop/work/project/OCR-label-ui/streamlit_image_label/frontend/1.jpeg"), image_path2base64_image("/Users/lixumin/Desktop/work/project/OCR-label-ui/streamlit_image_label/frontend/1.jpeg")][i%2], f"sdafadsfasdf{i}"] for i in range(1)], 
            columns=["id", "status", "image", "text"]
        )
        st.session_state.data_df = st.session_state.data_df.sort_values(by=['status', 'id'])

    if 'current_value' not in st.session_state:
        # 输出新的第一个状态为false的行数据
        status_false = st.session_state.data_df[st.session_state.data_df['status'] == False]
        if not status_false.empty:
            st.session_state.current_row = status_false.iloc[0]
        else:
            st.session_state.current_row = st.session_state.data_df.iloc[0]
            done()

    if "choose_id" not in st.session_state:
        st.session_state.choose_id = None

    data_col1, data_col2 = st.columns(2)
    with data_col1:
        # 在此创建占位符
        updated_data_df = st.dataframe(
            st.session_state.data_df,
                column_config={
                    "id": st.column_config.TextColumn(
                        "图片ID",
                        help="图片ID",
                        width="medium",
                    ),
                    "status": st.column_config.CheckboxColumn(
                        "是否修改",
                        help="是否修改",
                        width="small",
                        default=False,
                    ),
                    "image": st.column_config.ImageColumn(
                        "图片",
                        help="图片",
                        width="small",
                    ),
                    "text": st.column_config.TextColumn(
                        "文本",
                        help="文本",
                        width="large",
                        required=True,
                    ),
                    # "text_bbox": st.column_config.TextColumn(
                    #     "文本框",
                    #     help="文本框",
                    #     width="medium",
                    #     required=True,
                    # ),
                },
                hide_index=True,
                height=300,
                width=2000
            )
        _col1, _col2 = st.columns(2)
        with _col1:
            choose_id = st.text_input(f"需要重新修改的图片ID",)
            if st.button("确认"):
                # 清空更新文本
                if choose_id in st.session_state.data_df['id'].values:
                    st.session_state.choose_id = choose_id
        
        if st.session_state.choose_id:
            st.session_state.current_row = st.session_state.data_df[st.session_state.data_df['id'] == st.session_state.choose_id].iloc[0]

    
        with _col2:
            # st.markdown(f"<h5 style='text-align: center; color: black;'>用户ID:{st.session_state.user_id}</h3>", unsafe_allow_html=True)
            st.text(f"用户ID：{st.session_state.user_id}")
            st.text(f"当前修改图片ID：{st.session_state.current_row['id']}")
            # st.button("顺时针旋转90˚", on_click=rotation(True))
            # st.button("逆时针旋转90˚", on_click=rotation(False))

    if "update_text" not in st.session_state:
        st.session_state.update_text = ""

    with data_col2:
        st.markdown(f"""
                <div style="display: flex; justify-content: center;">
                    <img src="{st.session_state.current_row['image']}" style="height: 450px;">
                </div>
            """, unsafe_allow_html=True)

    st.session_state.update_text = latex_render(fr"""{st.session_state.current_row["text"]}""")

    if st.session_state.update_text:
        # 提交后，找到当前行的id
        current_id = st.session_state.current_row['id']
        print("id:", current_id)

        # 使用id来定位该行并修改status为True
        row_index = st.session_state.data_df[st.session_state.data_df['id'] == current_id].index[0]
        
        # 更新该行的status为True
        st.session_state.data_df.at[row_index, 'status'] = True  # 将status更新为True
        
        # 如果你还想修改其他字段，像是text、text_bbox等，也可以类似地更新
        st.session_state.data_df.at[row_index, 'text'] = st.session_state.update_text
        
        st.session_state.data_df = st.session_state.data_df.sort_values(by=['status', 'id'])
        # 清空更新文本
        st.session_state.update_text = ""

        # 提交后，重复输出新的第一个状态为false的行数据
        status_false = st.session_state.data_df[st.session_state.data_df['status'] == False]
        if not status_false.empty:
            st.session_state.current_row = status_false.iloc[0]
        else:
            st.session_state.current_row = st.session_state.data_df.iloc[0]
        st.session_state.choose_id = None
        st.rerun()

image_label(st.session_state.current_row['image'])