import streamlit as st
import pandas as pd
from github import Github

# 页面设置
st.set_page_config(page_title="户型展示与搜索系统", layout="wide")
st.title("🏘️ 户型展示与搜索系统")

# 在 Streamlit Secrets 设置 GITHUB_TOKEN
# 创建位置：https://github.com/settings/tokens
token = st.secrets["GITHUB_TOKEN"]

# 1. 连接 GitHub API
g = Github(token)

# 2. 获取仓库和文件
repo = g.get_repo("NightShadowNian/ng")
file = repo.get_contents("南国鼎峰-户型案例.xlsx")

# 读取数据（实际使用时替换为您的Excel文件路径）
@st.cache_data
def load_data():
    # 这里用示例数据创建DataFrame，实际使用时替换为 pd.read_excel("your_file.xlsx")
    data = {
        "小区名称": ["盛天", "六峰华府", "盛天", "阳光家园", "六峰华府", "绿城雅苑"],
        "房号": ["2-802", "1-1-1104", "3-701", "5-1202", "2-903", "8-1503"],
        "风格": ["现代", "轻奢", "现代", "欧式", "轻奢", "新中式"],
        "备注": ["A户型", "B户型", "C户型", "D户型", "A户型", "E户型"],
        "地址": ["url1", "url2", "url3", "url4", "url5", "url6"]
    }
    # return pd.DataFrame(data)
    import base64
    decoded = base64.b64decode(content.content)
    return pd.read_excel(BytesIO(decoded))

    return load_private_excel(file)
    # return pd.read_excel(r"E:\win\桌面\南国鼎峰-户型案例.xlsx")

df = load_data()

# 侧边栏控制面板
with st.sidebar:
    st.subheader("系统模式")
    
    # 模式选择
    mode = st.radio(
        "选择系统模式：",
        ["户型展示系统", "搜索模式"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if mode == "户型展示系统":
        st.subheader("户型展示筛选")
        
        # 1. 小区名称下拉选择（含"全部"选项）
        communities = ["全部"] + sorted(df["小区名称"].unique().tolist())
        selected_community = st.selectbox(
            "选择小区名称：",
            communities,
            index=0  # 默认选择"全部"
        )
        
        # 2. 房号搜索框
        room_search = st.text_input("搜索房号：", placeholder="输入部分或完整房号")
        
    else:  # 搜索模式
        st.subheader("高级搜索")
        
        # 1. 风格搜索
        styles = ["全部"] + sorted(df["风格"].unique().tolist())
        selected_style = st.selectbox(
            "选择装修风格：",
            styles,
            index=0
        )
        
        # 2. 户型备注搜索
        remarks = ["全部"] + sorted(df["备注"].unique().tolist())
        selected_remark = st.selectbox(
            "选择户型备注：",
            remarks,
            index=0
        )

# 数据筛选逻辑
filtered_df = df.copy()

# 根据当前模式应用筛选条件
if mode == "户型展示系统":
    # 按小区筛选
    if selected_community != "全部":
        filtered_df = filtered_df[filtered_df["小区名称"] == selected_community]
    
    # 按房号搜索
    if room_search:
        filtered_df = filtered_df[filtered_df["房号"].str.contains(room_search)]
else:  # 搜索模式
    # 按风格筛选
    if selected_style != "全部":
        filtered_df = filtered_df[filtered_df["风格"] == selected_style]
    
    # 按户型备注筛选
    if selected_remark != "全部":
        filtered_df = filtered_df[filtered_df["备注"] == selected_remark]

# 展示结果
st.subheader(f"{mode} - 查询结果")
st.caption(f"当前模式: {mode} | 找到 {len(filtered_df)} 条匹配记录")

if not filtered_df.empty:
    # 优化表格显示
    st.dataframe(
        filtered_df.reset_index(drop=True),
        height=min(400, 35 * (len(filtered_df) + 1)),
        use_container_width=True,
        hide_index=True,
        column_config={
            "小区名称": st.column_config.TextColumn(width="small"),
            "房号": st.column_config.TextColumn(width="small"),
            "风格": st.column_config.TextColumn(width="small"),
            "备注": st.column_config.TextColumn("户型"),
            "地址": st.column_config.LinkColumn("详情链接")
        }
    )
    
    # 显示统计信息
    with st.expander("📊 数据统计"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("小区数量", filtered_df["小区名称"].nunique())
            st.metric("风格分布", ", ".join(filtered_df["风格"].value_counts().index.tolist()))
        
        with col2:
            st.metric("户型类型", filtered_df["备注"].nunique())
            st.metric("总记录数", len(filtered_df))
else:
    st.warning("⚠️ 未找到匹配的记录，请调整筛选条件")
    st.image("https://cdn.pixabay.com/photo/2017/02/12/21/29/false-2061131_960_720.png", width=200)

# 添加分隔线和说明
st.divider()
st.caption("### 使用说明：")
st.caption("**户型展示系统模式**")
st.caption("- 通过小区名称筛选特定小区的户型")
st.caption("- 通过房号搜索框模糊搜索特定房号")
st.caption("**搜索模式**")
st.caption("- 通过装修风格筛选特定风格的户型")
st.caption("- 通过户型备注筛选特定类型的户型")
