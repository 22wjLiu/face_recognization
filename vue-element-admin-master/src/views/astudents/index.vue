<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" placeholder="学生名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        查询
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-edit"
        @click="handleCreate"
      >
        添加
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
    >
      <el-table-column
        label="学号"
        prop="id"
        align="center"
        width="300"
      >
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column label="学生姓名" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button
            size="mini"
            style="margin-left:40px ;"
            type="danger"
            @click="handleDelete(row, $index)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      style="margin-left: 130px;"
      @pagination="getList"
    />

    <!-- 编辑弹窗 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px">

        <el-form-item label="学生姓名" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>


        <el-form-item v-if="dialogStatus !== 'create'" label="人脸特征">
          <!--内嵌 表格 -->
          <el-table
            :key="tableKey"
            v-loading="listLoading"
            :data="tempfeatures"
            border
            fit
            highlight-current-row
            height="300px"
            style="width: 100%;"
          >
            <el-table-column
              label="特征ID"
              prop="id"
              align="center"
              width="100"
            >
              <template slot-scope="{row}">
                <span>{{ row.id }}</span>
              </template>
            </el-table-column>

            <el-table-column label="图片" width="100px" align="center">
              <template slot-scope="{row}">
                <img style="height: 100px;" :src="getRequestHeader() + row.imgUrl" alt="">
              </template>
            </el-table-column>

            <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
              <template slot-scope="{row}">
                <el-button
                  size="mini"
                  style="margin-left:40px ;"
                  type="danger"
                  @click="handleFeatureDelete(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>

        <el-form-item v-if="dialogStatus !== 'create'" label="上传人脸特征">
          <el-upload
            class="avatar-uploader"
            :action="'http://127.0.0.1:5000/upload?s_id=' + temp.id"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="imageUrl" :src="getRequestHeader() + imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon" />
          </el-upload>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves'
import request from '@/utils/request'
import { getRequestHeader } from '@/utils/requestpath'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      imageUrl: '',
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      featureListLoading: false,
      listQuery: {
        page: 1,
        limit: 10,
        name: ''
      },
      showReviewer: false,
      temp: {
        id: undefined,
        name: ''
      },
      tempfeatures: [],
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '创建'
      },
      rules: {
        name: [{ required: true, message: '学生姓名不能为空', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getRequestHeader,
    getList() {
      this.listLoading = true
      request.get('student/queryStudentList', {
        params: this.listQuery
      }).then(response => {
        this.list = response.data
        this.total = response.total
        this.listLoading = false
      })
    },
    getFeatureList(id) {
      this.featureListLoading = true
      request.get('feature/queryFeatureList', {
        params: {
          sId: id
        }
      }).then(response => {
        this.tempfeatures = response.data
        this.featureListLoading = false
      })
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        name: ''
      }
    },
    handleCreate() {
      this.resetTemp() // 调用resetTemp方法，重置表单字段
      this.dialogStatus = 'create' // 设置对话框状态为'create'，表示创建
      this.dialogFormVisible = true /* 打开弹窗 */
      this.$nextTick(() => { // 在下一次 DOM 更新循环之后，清除表单验证
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          request.post('student/addStudent', this.temp).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '添加学生成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) { // 编辑操作
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.imageUrl = ''
      this.getFeatureList(this.temp.id)
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          request.post('student/updateStudent', this.temp).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '编辑成功！',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleFeatureDelete(row) {
      request.delete('feature/deleteById', {
        params: {
          id: row.id
        }
      }).then(() => {
        this.getFeatureList(this.temp.id)
        this.$notify({
          title: '成功',
          message: '删除成功！',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleDelete(row) {
      request.delete('student/deleteById', {
        params: {
          id: row.id
        }
      }).then(() => {
        this.getList()
        this.$notify({
          title: '成功',
          message: '删除成功！',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleAvatarSuccess(res) {
      this.imageUrl = res.data
      this.$notify({
        title: '成功',
        message: '添加人脸特征成功！',
        type: 'success',
        duration: 2000
      })
      this.getFeatureList(this.temp.id)
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
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
.filter-container .filter-item {
  margin-left: 10px;
}

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
