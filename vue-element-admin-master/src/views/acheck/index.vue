<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" placeholder="考勤名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.cId" placeholder="选择班级" clearable class="filter-item" style="width: 200px;">
        <el-option v-for="item in classList" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        查询
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        发起考勤
      </el-button>
    </div>

    <!-- 表格 -->
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column label="ID" prop="id" align="center" width="100">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column label="开始时间" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.createTime | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column label="截止时间" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.endTime | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column label="考勤名称" width="300px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="班级" width="100px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.cId }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="350px" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" style="margin-left:20px ;" @click="detailViews(row.id)">
            结果详情
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" style="margin-left:20px ;" @click="handleDelete(row,$index)">
            删除考勤
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <!-- 考勤发起弹窗 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temper" label-position="left" label-width="125px">
        <!-- prop="title 与规则绑定 -->

        <el-form-item label="考勤结束时间" prop="endTime">
          <el-date-picker v-model="temper.endTime" type="datetime" placeholder="请选择时间" />
        </el-form-item>

        <el-form-item label=" 考勤的名称" prop="name">
          <el-input v-model="temper.name" />
        </el-form-item>

        <el-form-item label="选择考勤班级" prop="cId">
          <el-select v-model="temper.cId" class="filter-item" placeholder="请选择">
            <el-option v-for="item in classList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='createCheck'?createData():updateData()">
          确定
        </el-button>
      </div>
    </el-dialog>

    <!-- 考勤详情弹窗 -->
    <el-dialog :title="dialogTitle" :visible.sync="detailFormVisible">

      <el-table
        :key="tableKey"
        v-loading="checkInfoListLoading"
        :data="checkList"
        border
        fit
        highlight-current-row
        height="500px"
        style="width: 100%;"
      >

        <el-table-column
          label="学号"
          prop="sId"
          align="center"
          width="200"
        >
          <template slot-scope="{row}">
            <span>{{ row.sId }}</span>
          </template>
        </el-table-column>

        <el-table-column
          label="学生姓名"
          prop="name"
          align="center"
          width="250"
        >
          <template slot-scope="{row}">
            <span>{{ row.name }}</span>
          </template>
        </el-table-column>

        <el-table-column
          label="考勤状态"
          prop="author"
          align="center"
          width="250"
        >
          <template slot-scope="{row}">
            <el-tag v-if="row.status == 0" type="info">未签到</el-tag>
            <el-tag v-else-if="row.status == 1" type="success">签到成功</el-tag>
          </template>
        </el-table-column>

      </el-table>

      <el-upload
        class="avatar-uploader"
        :action="getUploadHeader() + 'recognize?c_id=' + listQueryInfos.cId"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
      >
        <img v-if="imageUrl" :src="getRequestHeader() + imageUrl" class="avatar">
        <i v-else class="el-icon-plus avatar-uploader-icon" />
      </el-upload>
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import request from '@/utils/request'
import { parseTime } from '@/utils'
import { getRequestHeader, getUploadHeader } from '@/utils/requestpath'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      imageUrl: '',
      dialogVisible: false,
      tableKey: 0,
      list: null,
      classList: null,
      checkList: null,
      total: 0,
      listLoading: true,
      checkInfoListLoading: false,
      listQuery: {
        page: 1,
        limit: 20,
        name: ''
      },
      listQueryInfos: { /** 考勤详情 */
        cId: ''
      },
      temper: {
        id: undefined,
        createTime: '',
        endTime: '',
        name: '', /** 考勤名称 */
        className: '',
        cid: 0/** 班级id */
      },
      dialogFormVisible: false,
      detailFormVisible: false,
      ImgFormVisible: false,
      dialogStatus: '',
      dialogTitle: '详细信息',
      dialogUploadimg: '上传考勤图片',
      textMap: {
        update: '编辑',
        create: '创建',
        createCheck: '创建考勤'
      },
      pvData: [],
      rules: {
        cId: [{ required: true, message: '请填写待考勤班级', trigger: 'blur' }],
        endTime: [{ required: true, message: '请填写截止时间', trigger: 'blur' }],
        name: [{ required: true, message: '请填写考勤名称', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getAllClass()
    this.getList()
  },
  methods: {
    parseTime,
    getRequestHeader,
    getUploadHeader,
    // 添加考勤列表
    getList() {
      this.listLoading = true
      request.get('check/queryCheckLists', {
        params: this.listQuery
      }).then(response => {
        this.list = response.data
        this.total = response.total
        this.listLoading = false // 确保加载状态关闭
      })
    },
    // 添加考勤状态学生列表
    getCheckList() {
      this.checkInfoListLoading = true
      request.get('check/queryCheckInfos', {
        params: this.listQueryInfos
      }).then(response => {
        this.checkList = response.data
        this.checkInfoListLoading = false // 确保加载状态关闭
      })
    },
    getAllClass() {
      request.get('class/queryAllClassIdAndName').then(response => {
        this.classList = response.data
      })
    },
    handleFilter() { /** 筛选 */
      this.listQuery.page = 1
      this.getList()
    },
    resetTemp() {
      this.temper = {
        name: '',
        createTime: '',
        endTime: '',
        cId: ''
      }
    },
    // 显示发起考勤弹窗
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'createCheck'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    // 添加考勤
    createData() {
      this.temper.createTime = new Date().toLocaleString().replaceAll('/', '-')
      this.temper.endTime = new Date(this.temper.endTime).toLocaleString().replaceAll('/', '-')
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          request.post('check/addCheckList', this.temper).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '添加考勤成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    updateImgData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          request.post('student/updateStudent', this.temp).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '考勤图片上传成功！',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    // 删除考勤
    handleDelete(row) {
      request.delete('check/deleteById', {
        params: {
          id: row.id
        }
      }).then(() => {
        this.getList()
        this.$notify({
          title: '成功',
          message: '删除考勤成功！',
          type: 'success',
          duration: 2000
        })
      })
    },
    detailViews(cId) { // 考勤详细信息
      this.resetTemp()
      this.dialogTitle = '考勤详细信息'
      this.detailFormVisible = true
      this.listQueryInfos.cId = cId
      this.getCheckList()
    },
    handleAvatarSuccess(res) { /* 考勤图片上传 */
      this.imageUrl = res.data
      this.$notify({
        title: '成功',
        message: '识别成功！',
        type: 'success',
        duration: 2000
      })
      this.getCheckList()
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
        return false
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
        return false
      }
      this.$notify({
        title: '成功',
        message: '提交上传请求成功，请等待服务器响应！',
        type: 'success',
        duration: 2000
      })
      return isJPG && isLt2M
    }
  }
}
</script>

<style scoped>
 .avatar-uploader >>> .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader >>> .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>

