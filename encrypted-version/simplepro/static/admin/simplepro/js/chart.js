/**
 封装echarts在vue中使用
 **/
var t = null;
Vue.component('echarts', {
    props: ['option', 'style'],
    data: function () {
        return {}
    },
    mounted: function () {
        this.$nextTick(function () {
            var el = this.$el;
            var chart = echarts.init(el, 'macarons');
            chart.setOption(this.option || {});
            this.chart = chart;

            //延迟500ms 改善卡顿
            if (t) {
                window.clearTimeout(t);
            }
            t = setTimeout(() => {
                window.addEventListener('resize', () => chart.resize());
            }, 1000);

        });
    },
    watch: {
        option: {
            deep: true,
            handler: function (newValue, oldValue) {
                //option发生改变，就重新渲染
                if (!this.chart) {
                    return;
                }
                if (newValue) {
                    this.chart.setOption(newValue);
                } else {
                    this.chart.setOption({});
                }
            }
        }
    },
    template: '<div :style="style">{{option}}</div>'
})