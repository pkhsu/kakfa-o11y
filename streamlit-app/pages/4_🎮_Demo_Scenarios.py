import streamlit as st
import subprocess
import time
import pandas as pd
import os
from datetime import datetime
import sys

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import initialize_language
from content.translations import get_text

st.set_page_config(
    page_title="Demo Scenarios",
    page_icon="🎮",
    layout="wide"
)

language = initialize_language()

st.title(get_text(language, "scenarios_title"))
st.markdown(f"### {get_text(language, 'scenarios_header')}")

def run_command(command, timeout=30):
    """Execute shell command and return output"""
    try:
        # We need to navigate to the parent directory to run docker-compose commands
        result = subprocess.run(
            f"cd .. && {command}", 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

# Scenario selection
st.markdown(f"### {get_text(language, 'choose_scenario')}")
scenario_options = {
    get_text(language, "scenario_a_title"): "scenario_a",
    get_text(language, "scenario_b_title"): "scenario_b",
    get_text(language, "scenario_c_title"): "scenario_c",
    get_text(language, "scenario_d_title"): "scenario_d"
}

selected_scenario_title = st.selectbox(
    get_text(language, "select_scenario"),
    list(scenario_options.keys())
)

scenario_key = scenario_options[selected_scenario_title]

def display_scenario_a():
    st.markdown(f"## {get_text(language, 'scenario_a_header')}")
    st.markdown(f"### {get_text(language, 'scenario_a_objectives_header')}")
    st.markdown(get_text(language, "scenario_a_objectives_content"))
    
    st.markdown(f"### {get_text(language, 'scenario_a_guide_header')}")
    
    with st.expander(get_text(language, "scenario_a_step1_header")):
        st.markdown(get_text(language, "scenario_a_step1_goal"))
        
        if st.button(get_text(language, "scenario_a_step1_button"), key="start_env"):
            with st.spinner(get_text(language, "scenario_a_step1_spinner")):
                returncode, stdout, stderr = run_command("docker compose up -d")
                if returncode == 0:
                    st.success(get_text(language, "scenario_a_step1_success"))
                    st.code(stdout)
                else:
                    st.error(f"{get_text(language, 'scenario_a_step1_error')} {stderr}")
        
        st.code(get_text(language, "scenario_a_step1_manual"), language="bash")
    
    with st.expander(get_text(language, "scenario_a_step2_header")):
        st.markdown(get_text(language, "scenario_a_step2_goal"))
        
        if st.button(get_text(language, "scenario_a_step2_button"), key="check_status"):
            with st.spinner(get_text(language, "scenario_a_step2_spinner")):
                returncode, stdout, stderr = run_command("docker compose ps")
                st.code(stdout)
                
                services = ["kafka", "zookeeper", "prometheus", "grafana", "otel-collector"]
                status_data = []
                
                for service in services:
                    returncode, stdout, stderr = run_command(f"docker compose ps {service}")
                    status = "Running" if "Up" in stdout else "Down"
                    status_data.append({
                        get_text(language, "scenario_a_step2_service_col"): service, 
                        get_text(language, "scenario_a_step2_status_col"): status
                    })
                
                st.dataframe(pd.DataFrame(status_data))
    
    with st.expander(get_text(language, "scenario_a_step3_header")):
        st.markdown(get_text(language, "scenario_a_step3_goal"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(get_text(language, "scenario_a_step3_producer_button"), key="python_prod"):
                with st.spinner(get_text(language, "scenario_a_step3_spinner")):
                    returncode, stdout, stderr = run_command("docker compose logs --tail=20 python-producer")
                    st.code(stdout)
        
        with col2:
            if st.button(get_text(language, "scenario_a_step3_consumer_button"), key="go_cons"):
                with st.spinner(get_text(language, "scenario_a_step3_spinner")):
                    returncode, stdout, stderr = run_command("docker compose logs --tail=20 go-consumer")
                    st.code(stdout)
    
    with st.expander(get_text(language, "scenario_a_step4_header")):
        st.markdown(get_text(language, "scenario_a_step4_goal"))
        
        st.markdown(f"**{get_text(language, 'scenario_a_step4_access_header')}**")
        st.markdown(get_text(language, "scenario_a_step4_url"))
        st.markdown(get_text(language, "scenario_a_step4_user"))
        st.markdown(get_text(language, "scenario_a_step4_pass"))
        
        if st.button(get_text(language, "scenario_a_step4_button"), key="open_grafana"):
            st.markdown(get_text(language, "scenario_a_step4_link"))
            st.info(get_text(language, "scenario_a_step4_info"))

def display_scenario_b():
    st.markdown(f"## {get_text(language, 'scenario_b_header')}")
    st.markdown(f"### {get_text(language, 'scenario_b_objectives_header')}")
    st.markdown(get_text(language, "scenario_b_objectives_content"))

    with st.expander(get_text(language, "scenario_b_step1_header")):
        st.markdown(get_text(language, "scenario_b_step1_goal"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(get_text(language, "scenario_b_step1_pause_button"), key="pause_kafka"):
                with st.spinner(get_text(language, "scenario_b_step1_pause_spinner")):
                    returncode, _, stderr = run_command("docker compose pause kafka")
                    if returncode == 0:
                        st.success(get_text(language, "scenario_b_step1_pause_success"))
                    else:
                        st.error(f"{get_text(language, 'scenario_b_step1_pause_error')} {stderr}")
        
        with col2:
            if st.button(get_text(language, "scenario_b_step1_unpause_button"), key="unpause_kafka"):
                with st.spinner(get_text(language, "scenario_b_step1_unpause_spinner")):
                    returncode, _, stderr = run_command("docker compose unpause kafka")
                    if returncode == 0:
                        st.success(get_text(language, "scenario_b_step1_unpause_success"))
                    else:
                        st.error(f"{get_text(language, 'scenario_b_step1_unpause_error')} {stderr}")

def display_scenario_c():
    st.markdown(f"## {get_text(language, 'scenario_c_header')}")
    st.markdown(f"### {get_text(language, 'scenario_c_objectives_header')}")
    st.markdown(get_text(language, "scenario_c_objectives_content"))

    with st.expander(get_text(language, "scenario_c_step1_header")):
        st.markdown(get_text(language, "scenario_c_step1_goal"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(get_text(language, "scenario_c_step1_stop_button"), key="stop_kafka"):
                with st.spinner(get_text(language, "scenario_c_step1_stop_spinner")):
                    returncode, _, stderr = run_command("docker compose stop kafka")
                    if returncode == 0:
                        st.success(get_text(language, "scenario_c_step1_stop_success"))
                    else:
                        st.error(f"{get_text(language, 'scenario_c_step1_stop_error')} {stderr}")
        
        with col2:
            if st.button(get_text(language, "scenario_c_step1_start_button"), key="start_kafka"):
                with st.spinner(get_text(language, "scenario_c_step1_start_spinner")):
                    returncode, _, stderr = run_command("docker compose start kafka")
                    if returncode == 0:
                        st.success(get_text(language, "scenario_c_step1_start_success"))
                    else:
                        st.error(f"{get_text(language, 'scenario_c_step1_start_error')} {stderr}")

def display_scenario_d():
    st.markdown(f"## {get_text(language, 'scenario_d_header')}")
    st.markdown(f"### {get_text(language, 'scenario_d_objectives_header')}")
    st.markdown(get_text(language, "scenario_d_objectives_content"))

    with st.expander(get_text(language, "scenario_d_step1_header")):
        st.markdown(get_text(language, "scenario_d_step1_goal"))
        
        num_consumers = st.slider(get_text(language, "scenario_d_step1_label"), 1, 5, 1)
        
        if st.button(get_text(language, "scenario_d_step1_button"), key="scale_consumers"):
            with st.spinner(get_text(language, "scenario_d_step1_spinner")):
                command = f"docker compose up -d --scale python-consumer={num_consumers} --no-recreate"
                returncode, stdout, stderr = run_command(command)
                if returncode == 0:
                    st.success(get_text(language, "scenario_d_step1_success"))
                    st.code(stdout)
                else:
                    st.error(f"{get_text(language, 'scenario_d_step1_error')} {stderr}")


# Display selected scenario
if scenario_key == "scenario_a":
    display_scenario_a()
elif scenario_key == "scenario_b":
    display_scenario_b()
elif scenario_key == "scenario_c":
    display_scenario_c()
elif scenario_key == "scenario_d":
    display_scenario_d()

# Common utilities section
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 🛠️ 常用工具")
else:
    st.markdown("### 🛠️ Common Utilities")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 All Logs" if language == "English" else "📋 所有日誌"):
        with st.spinner("Fetching all logs..." if language == "English" else "獲取所有日誌..."):
            returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=50")
            st.code(stdout[-5000:])  # Limit output size

with col2:
    if st.button("🔄 Restart All" if language == "English" else "🔄 重啟全部"):
        with st.spinner("Restarting all services..." if language == "English" else "重啟所有服務..."):
            returncode, stdout, stderr = run_command("cd .. && docker compose restart")
            if returncode == 0:
                st.success("✅ All services restarted" if language == "English" else "✅ 所有服務已重啟")
            else:
                st.error(f"❌ Restart failed: {stderr}")

with col3:
    if st.button("🧹 Clean Up" if language == "English" else "🧹 清理環境"):
        with st.spinner("Cleaning up..." if language == "English" else "清理中..."):
            returncode, stdout, stderr = run_command("cd .. && docker compose down")
            if returncode == 0:
                st.success("✅ Environment cleaned up" if language == "English" else "✅ 環境已清理")
            else:
                st.error(f"❌ Cleanup failed: {stderr}")

# Tips and best practices
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 💡 提示與最佳實務")
    st.info("""
    **學習提示:**
    - 🎯 每個情境都有明確的學習目標，按順序完成效果最佳
    - 📊 在執行操作前後檢查 Grafana 儀表板
    - 📝 記錄觀察到的指標變化
    - 🔄 重複練習以加深理解
    """)
else:
    st.markdown("### 💡 Tips & Best Practices")
    st.info("""
    **Learning Tips:**
    - 🎯 Each scenario has clear learning objectives - follow them in order
    - 📊 Check Grafana dashboards before and after operations
    - 📝 Record the metric changes you observe
    - 🔄 Repeat exercises to deepen understanding
    """)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 