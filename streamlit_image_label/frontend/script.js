
// Streamlit组件通信API
function sendMessageToStreamlitClient(type, data) {
    const outData = Object.assign({
        isStreamlitMessage: true,
        type: type,
    }, data);
    window.parent.postMessage(outData, "*");
}

const Streamlit = {
    setComponentReady: function() {
        sendMessageToStreamlitClient("streamlit:componentReady", {apiVersion: 1});
    },
    setFrameHeight: function(height) {
        sendMessageToStreamlitClient("streamlit:setFrameHeight", {height: height});
    },
    setComponentValue: function(value) {
        sendMessageToStreamlitClient("streamlit:setComponentValue", {value: value});
    },
    RENDER_EVENT: "streamlit:render",
    events: {
        addEventListener: function(type, callback) {
            window.addEventListener("message", function(event) {
                if (event.data.type === type) {
                    callback(event);
                }
            });
        }
    }
};

// 发送标注数据到Streamlit·
function sendValue(value) {
    Streamlit.setComponentValue(value);
}

// 处理Streamlit发送的渲染事件
function onRender(event) {
    if (!window.rendered) {
        // 从Streamlit接收图片数据
        if (event.data.args && event.data.args.data) {
            const imageBase64 = event.data.args.data;
            console.log("接收到图片数据，长度:", imageBase64.length);
            loadImageFromStreamlit(imageBase64);
        }
        window.rendered = true;
    }
}

// 注册渲染事件监听器
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

// 组件初始化
Streamlit.setComponentReady();
Streamlit.setFrameHeight(1000);