const quickColors = ['rgb(105, 192, 255)', 'rgb(149, 222, 100)', 'rgb(255, 156, 110)', 'rgb(179, 127, 235)', 'rgb(255, 214, 102)', 'rgb(92, 219, 211)', 'rgb(255, 133, 192)', 'rgb(255, 192, 105)'];
window.colorMappers = window.colorMappers || {};
window.getColor = function (id) {
    let val = colorMappers[id];
    if (val) {
        return val;
    }
    let color = 'color: ' + quickColors[Math.floor(Math.random() * quickColors.length)];
    colorMappers[id] = color;
    return color;
}

Vue.component('split-layout', {
    data() {
        return {
            isSmall: false,
        }
    },
    mounted() {
        this.resize();
        window.addEventListener('resize', this.resize);
    },
    //销毁
    beforeDestroy() {
        window.removeEventListener('resize', this.resize);
    },
    methods: {
        getViewPortWidth() {
            return document.documentElement.clientWidth || document.body.clientWidth;
        },
        resize() {
            let width = this.getViewPortWidth();
            this.isSmall = width <= 768;
        }
    },
    template: `
    <el-row>
        <el-col :span="isSmall?24:18">
            <slot name="left"></slot>
        </el-col>
        <el-col :span="isSmall?24:6">
            <div v-if="isSmall" style="margin-top: 10px;"></div>
            <div :style="!isSmall?'padding-left:10px;':''">
                <slot name="right"></slot>
            </div>
        </el-col>
    </el-row>
    `,
})