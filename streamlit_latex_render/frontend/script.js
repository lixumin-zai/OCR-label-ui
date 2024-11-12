
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

let text;

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

function backText() {
    const inputField = document.getElementById('input_text');
    // 弹出确认框，询问用户是否要修改
    const userConfirmed = window.confirm("你确定要还原文本吗？");

    // 如果用户点击"确定"，则修改输入框的内容
    if (userConfirmed) {
        inputField.value = text;
        // 手动触发 input 事件
        const inputEvent = new Event('input', {
            'bubbles': true,
            'cancelable': true
        });
        inputField.dispatchEvent(inputEvent);
    }
}

function processText(text) {
    // Step 1: Handle <blank> tags
    text = text.replace(/<blank>(.*?)<\/blank>/g, (match, p1) => `\\underline{${p1}}`);

    // Handle <handwritten> tags
    text = text.replace(/<handwritten>(.*?)<\/handwritten>/g, (match, content) => {
        // Check if there's a $$ formula inside
        if (content.includes('$')) {
            content = content.replace(/\$(.*?)\$/g, (formulaMatch, formulaContent) => {
                return `$\\textcolor{red}{${formulaContent}}$`;
            });
        }
        return `<span style="color: red;">${content}</span>`;
    });

    // Handle <del> tags
    text = text.replace(/<del>(.*?)<\/del>/g, (match, content) => {
        // Check if there's a $$ formula inside
        if (content.includes('$')) {
            content = content.replace(/\$(.*?)\$/g, (formulaMatch, formulaContent) => {
                return `$\\enclose{horizontalstrike}{${formulaContent}}$`;
            });
        }
        return `<del>${content}</del>`;
    });

    return text;
}

function update() {
    const inputField = document.getElementById('input_text');
    sendValue(inputField.value);
}

function addText(start_text, end_text) {
    const textarea = document.getElementById('input_text');

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    // 获取选中的文本内容
    const choose_text = textarea.value;

    // 在选中的文本前后添加 $
    const newText = choose_text.slice(0, start) + start_text + choose_text.slice(start, end) + end_text + choose_text.slice(end);

    // 更新 textarea 的内容
    // textarea.value = newText;
    // textarea.setRangeText(newText);
    textarea.setRangeText(start_text + choose_text.slice(start, end) + end_text, start, end);
    
    // 恢复选中区域
    textarea.setSelectionRange(start + start_text.length, end + start_text.length);

    // 隐藏菜单
    menu.style.display = "none";
    
    // 聚焦到 textarea
    textarea.focus();

    // 手动触发 input 事件
    // const inputEvent = new Event('input', {
    //     'bubbles': true,
    //     'cancelable': true
    // });
    // textarea.dispatchEvent(inputEvent);
    setTimeout(() => {
        const event = new Event('input', { bubbles: true, cancelable: true });
        textarea.dispatchEvent(event);
    }, 0);
}

function onRender(event) {
    if (!window.rendered) {
        
        // const text = "$\\textcolor{red}{{你好，(-1,-\\dfrac{\\sqrt{3}}{3})\\cup(\\dfrac{\\sqrt{3}}{3},1)}}$ \\sout{nihao}"
        let script = document.createElement('script');
        const textarea = document.getElementById('input_text');
        const mainElement = document.getElementById('main');

        textarea.value = text;

        script.src = "https://cdn.jsdelivr.net/npm/mathpix-markdown-it@2.0.4/es5/bundle.js";
        document.head.append(script);

        // 首次渲染
        script.onload = function() {
            const isLoaded = window.loadMathJax();
            if (isLoaded) {
                console.log('Styles loaded!')
            }
            const modifiedText = textarea.value;  
            const options = {
                htmlTags: true
            };
            // 假设 window.render 是一个渲染函数，将文本转换为 HTML
            const html = window.render(processText(modifiedText), options);
            mainElement.innerHTML = html; // 更新内容
        };

        const menu = document.getElementById("menu");

        // 显示菜单
        textarea.addEventListener("mouseup", (event) => {
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            
            // 判断是否有选中的文本
            if (start !== end) {
                // 获取 textarea 中选中文本的屏幕坐标
                const rect = textarea.getBoundingClientRect();
                
                // 设置菜单的位置并显示菜单
                menu.style.left = `${event.pageX}px`;
                menu.style.top = `${event.pageY + 10}px`;
                menu.style.display = "block";
            } else {
                // 如果没有选中文本，隐藏菜单
                menu.style.display = "none";
            }
        });

        // 监听键盘事件以实现撤销和重做
        // textarea.addEventListener("keydown", (event) => {
        //     // 检查 Ctrl+Z (撤销) 和 Ctrl+Y 或 Ctrl+Shift+Z (重做)
        //     if ((event.ctrlKey || event.metaKey) && event.key === 'z') {
        //         event.preventDefault();
        //         undo();
        //     } else if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'z') {
        //         event.preventDefault();
        //         redo();
        //     }
        // });

        // 点击其他地方时隐藏菜单
        document.addEventListener("click", (event) => {
            if (event.target !== textarea && event.target.parentNode !== menu) {
                menu.style.display = "none";
            }
        });

        // input 修改后进行渲染
        textarea.addEventListener('input', function() {
            const modifiedText = textarea.value;  
            const options = {
                htmlTags: true
            };
            // 假设 window.render 是一个渲染函数，将文本转换为 HTML
            const html = window.render(processText(modifiedText), options);
            mainElement.innerHTML = html; // 更新内容
        })
        window.rendered = true
    }
}
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

Streamlit.setComponentReady();
Streamlit.setFrameHeight(400);

// 🐑老板请我吃烤鸡了，我要加倍努力工作