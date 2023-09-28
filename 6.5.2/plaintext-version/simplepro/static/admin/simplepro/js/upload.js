Vue.component('Uploader', {
    props: ['value'],
    data() {
        return {
            showFile: false
        }
    },
    methods: {
        fileChange(e) {
            this.showFile = false;
            this.$emit('input', e.target.files[0]);
            console.log(e.target.files[0]);
        },
        selectFile() {
            this.showFile = true;
            this.$nextTick(() => {
                this.$refs.file.click();
            });
        }
    },
    template: `
    <div tabindex="0" class="el-upload el-upload--text">
        <div class="el-upload-dragger" @click="selectFile()">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        </div>
        <div class="el-upload__tip" v-if="value" v-text="value.name"></div>
        <input @change="fileChange($event)" v-if="showFile" ref="file" type="file" name="file" class="el-upload__input">
    </div>
    `
});