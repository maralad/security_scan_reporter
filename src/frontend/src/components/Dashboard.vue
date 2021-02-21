<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand :to="{name: 'dashboard'}">Coding Test</b-navbar-brand>

    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item :to="{name: 'logout'}">Logout</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  
    <!-- Styled -->
  <div class="container">
    <br>
    <div class="large-12 medium-12 small-12 cell">
      <label>Choose a Nessus file to upload
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
        <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
  <!-- The report-->
  <br>
    <b-container  class="bv-example-row" >
    <strong><b-row cols-lg="7">
      <b-col>Report Name</b-col>
      <b-col>Scan Date</b-col>
      <b-col>Plugins Run Count</b-col>
      <b-col>Warning Severity Count</b-col>
      <b-col>Minor Severity Count</b-col>
      <b-col>Major Severity Count</b-col>
       <b-col>Critical Severity Count</b-col>
    </b-row>
    </strong>
  </b-container>
    <b-container  class="bv-example-row">
    <b-row cols="7">
      <b-col class="p-3 bg-info">{{report_header.report_name}}</b-col>
      <b-col class="p-3 bg-info">{{report_header.scan_date}}</b-col>
      <b-col class="p-3 bg-info">{{report_header.plugin_check_count}}</b-col>
      <b-col class="p-3 bg-info">{{report_header.severity_level_warning_count}}</b-col>
      <b-col class="p-3 bg-info">{{report_header.severity_level_minor_count}}</b-col>
      <b-col class="p-3 bg-info">{{report_header.severity_level_major_count}}</b-col>
  <b-col class="p-3 bg-info">{{report_header.severity_level_critical_count}}</b-col>
    </b-row>
  </b-container>
  <br>
    <b-container  class="bv-example-row">
    <strong><b-row cols="6">
      <b-col >Severity Level</b-col>
      <b-col >Plugin Name</b-col>
      <b-col >Plugin Family</b-col>
      <b-col >Plugin Id</b-col>
      <b-col >Description</b-col>
    <b-col >Action</b-col>
    </b-row></strong>
  </b-container>
  <b-container v-for="rep in report" :key="rep.plugin_id" class="bv-example-row" >
    <b-row cols-lg="6">
      <b-col class="p-3 bg-info">{{rep.severity}}</b-col>
      <b-col class="p-3 bg-info">{{rep.plugin_name}}</b-col>
      <b-col class="p-3 bg-info">{{rep.plugin_family}}</b-col>
      <b-col class="p-3 bg-info">{{rep.plugin_id}}</b-col>
      <b-col class="p-3 bg-info">
        <div>
        <!-- Using modifiers -->
        <b-button v-b-toggle.collapse-2 class="m-1">Toggle To Read</b-button>
        <b-collapse id="collapse-2">
        <b-card>{{rep.description}}</b-card>
        </b-collapse>
        </div>
        </b-col>
      <b-col class="p-3 bg-info">
        <div>
        <!-- Using modifiers -->
        <b-button v-b-toggle.collapse-2 class="m-1">Toggle To Read</b-button>
        <b-collapse id="collapse-2">
        <b-card>{{rep.action}}</b-card>
        </b-collapse>
        </div>

      </b-col>
  
    </b-row>
    <hr>
  </b-container>

  <br>

 

  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Dashboard',
   data(){
      return {
        file: '',
        report:[],
        report_header:[]
       
      }
    },

    methods: {
      submitFile(){
            let formData = new FormData();
            formData.append('file', this.file);
                //trying to use token to authenticate :(
                // const config = {
                //         headers: { Authorization: `Bearer ${localStorage.auth}` }
                //     };

                axios.post( 'http://127.0.0.1:8000/nessus_file',
                formData,
                //config,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
              }
            ).then(response => {
              //console.log(response.data)

              this.report=response.data.items_found;
              this.report_header=response.data;

              
        
      }).catch(error => {
        this.showError = true;
        this.errors = error.response.data.non_field_errors;
        
      })
      },
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }
    }
  }


</script>

<style scoped>
</style>
