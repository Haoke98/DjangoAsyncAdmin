//处理自定义方法字段和对话框、和共用组件

function render(el, value) {
    let val = value;
    if (typeof (val) === 'undefined') {
        val = '';
    }
    return new Vue({
        el: el,
        template: `<span class="cell-btn">${val}<slot></slot></span>`
    })
}

Vue.component('HtmlRender', {
    props: ['html'],
    watch: {
        html(newValue) {
            this.vm = render(this.vm.$el, newValue);
        }
    },
    data() {
        return {
            show: false
        }
    },
    methods: {
        renderHtml() {
            //调用vue来渲染
            this.vm = render(this.$refs.cell, this.html);
        }
    },
    mounted() {
        this.$nextTick(() => this.renderHtml());
    },
    template: `<div  ref="cell"></div>`

});

Vue.component('ModalDialog', {
    props: ['data'],
    data() {
        return {
            visible: false,
        }
    },
    watch: {
        visible(val) {
            if (val) {
                window.currentModal = this;
            }
        }
    },
    methods: {
        showDialog() {
            console.log('showDialog')
            this.visible = true;
        },
        close() {
            this.visible = false;
        }
    },
    template: `
        <div>
        <div @click="showDialog()">
            <HtmlRender :html="data.cell"/>
        </div>
        <el-dialog
          :title="data.title"
          :visible.sync="visible"
          :width="data.width">
          <div :style="{height:data.height,overflow:'auto'}" v-cloak>
            
            <iframe v-if="visible&&data.url" :src="data.url" frameborder="0" width="100%" height="100%"></iframe>
            <el-alert v-if="visible&&!data.url" type="error" title="请设置ModalDialog的url"></el-alert>
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button v-if="data.show_cancel" size="small" @click="visible = false">取 消</el-button>
          </span>
        </el-dialog>
        </div>
    `
});

Vue.component('func', {
    props: ['value', 'pk'],
    computed: {
        isMultipleCellDialog() {
            return this.value._type === 'MultipleCellDialog';
        },
        isObject() {
            return typeof this.value == 'object';
        },
        isCellMultipleAction() {
            return this.value._type === 'CellMultipleAction';
        }
    },
    template: `
    <div v-if="isMultipleCellDialog" style="display: flex;justify-content: space-around;">
        <ModalDialog v-for="item in value.modals" :key="item" :data="item"></ModalDialog>
    </div>
    <div v-else-if="isCellMultipleAction" style="display: flex;justify-content: space-around;">
        <CellAction v-for="item in value.actions" :value="item" :pk="pk"></CellAction>
    </div>
    <CellAction v-else-if="isObject&&value._type=='CellAction'" :value="value" :pk="pk"></CellAction>
    <ModalDialog v-else-if="isObject&&value._type=='ModalDialog'" :data="value"></ModalDialog>
    <HtmlRender v-else :html="value"/>
    `
});
Vue.component('CellAction', {
    props: ['value', 'pk'],
    template: `
    <div style="display: flex;justify-content: space-around;" @click="onTap()">
        <HtmlRender :html="value.text"></HtmlRender>
    </div>
    `,
    methods: {
        onTap() {
            //读取自定义按钮是否有confirm，如果有就弹出提示框
            let fun = app.toolbars.customButtons[this.value.action];
            if (typeof fun === "undefined") {
                //提示错误
                app.$message.error(`配置错误，请将"${this.value.action}"，加入到admin中的actions中`);
                return;
            }
            console.log(fun);
            if (fun.confirm) {
                let confirm = fun.confirm;
                this.$confirm(confirm, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.doAction(this.value.action);
                }).catch(() => {
                });
            } else {
                this.doAction(this.value.action);
            }
        },
        doAction(action) {
            console.log('doAction', this.value);
            console.log(`执行:${action}-${this.pk}`);
            let postData = {
                action: 'custom_action',
                key: action,
                all: 0,
                ids: this.pk
            }
            post(postData, app, true).then((data) => {
                //刷新界面
                app.onSubmit();
            });
        }
    }
})
//渲染layer的组件
Vue.component('layer', {
    props: ['value'],
    render(h) {
        return h('div', {
            domProps: {
                innerHTML: this.value
            }
        });
    }
});