//创建vue组件

Vue.component('player-btn', {
    props: ['src'],
    data(){
        return {
            visible: false,
        }
    },
    template: `
<div>
    <el-link @click="visible=true" type="primary" icon="el-icon-video-play">播放</el-link>
    <player-dialog @close="visible=false" :visible="visible" :src="src"></player-dialog>
</div>
    `
});
Vue.component('player-dialog', {
    props: ['src', 'visible'],
    data() {
        return {
            id: `player_${new Date().getTime()}`,
        }
    },
    watch: {
        visible(val) {
            if (val) {
                this.$nextTick(() => {
                    this.initPlayer();
                });
            }
        }
    },
    methods: {
        handleClose() {
            this.$emit('close');
            this.palyer.destroy(true);
        },
        initPlayer() {
            console.log(this.src)
            this.palyer = new xgplayer({
                id: this.id,
                url: this.src,
                autoplay: true,
            });
            // this.palyer.play();
        }
    },
    template: `
<el-dialog
    :visible.sync="visible"
    title="视频播放器"
    width="635px"
    :before-close="handleClose">
    <div v-if="visible" :id="id"></div>
</el-dialog>`,
});