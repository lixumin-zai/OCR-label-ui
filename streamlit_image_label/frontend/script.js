
// Borrowed minimalistic Streamlit API from Thiago
// https://discuss.streamlit.io/t/code-snippet-create-components-without-any-frontend-tooling-no-react-babel-webpack-etc/13064
function sendMessageToStreamlitClient(type, data) {
    // console.log(type, data)
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
                    // console.log(event.data.args.data)
                    text = event.data.args.data
                    callback(event);
                }
            });
        }
    }
}

function sendValue(value) {
    Streamlit.setComponentValue(value);
}

function onRender(event) {
    if (!window.rendered) {
        
        
        window.rendered = true
    }
}
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

Streamlit.setComponentReady();
Streamlit.setFrameHeight(1000);

// 🐑老板请我吃烤鸡了，我要加倍努力工作