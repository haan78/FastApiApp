<template>
  <label :title="title" :class="disabled ? 'disabled_status' : 'active_status'">
    <input
      :disabled="disabled"
      ref="uploadField"
      type="file"
      @change="change()"
      style="display: none"
      :accept="accept"
    />
    <slot></slot>
  </label>
</template>
<style lang="scss" scoped>
$colorback: rgb(9, 116, 126);
$colorhover:  rgb(28, 150, 161);
$coloractive: rgb(124, 208, 216);
$colorfront: white;

$colordis: lightgray;
$colorborder: rgb(7, 78, 95);
$minborder: 0.1em;
$fontsize: 0.9em;
$padstep :0.73em;
$btnratio:2;

label {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Edge, Opera and Firefox */

  font-size: $fontsize;
  display: inline-block;    
  white-space: nowrap;
  padding-top: $padstep;
  padding-bottom: $padstep;
  padding-left: 2 * $padstep;
  padding-right: 2 * $padstep;
  border-radius: 3 * $minborder;

  &.disabled_status {
    cursor: no-drop;
    background-color: $colordis;    
    color: $colorfront;
    border: $minborder solid $colorborder;    
  }

  &.active_status {
    cursor: pointer;
    background-color: $colorback;
    color: $colorfront;    
    border: $minborder solid $colorborder;

    &:hover {
      background-color: $colorhover;
    }

    &:active {
      background-color: $coloractive;
    }
  }
}
</style>

<script>
export default {
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    fieldPrefix: {
      type: String,
      default: "file",
    },
    limit: {
      type: Number,
      default: 1,
    },
    title: {
      type: String,
      default: null,
    },
    accept: {
      type: String,
      default: "*/*",
    },
  },
  data() {
    return {};
  },
  emits: ["request", "error"],
  methods: {
    change() {
      let self = this;
      var input = self.$refs.uploadField;

      if (input.files.length > self.limit) {
        self.$emit(
          "error",
          new Error("Maximum file upload limit is " + self.limit)
        );
      }

      if (input.files.length > 0) {
        var files = [];

        const formData = new FormData();
        for (var i = 0; i < input.files.length; i++) {
          var n = self.fieldPrefix + (input.files.length > 1 ? (i + 1) : '' ) ;
          files.push({
            input:n,
            name:input.files[i].name,
            preview:URL.createObjectURL(input.files[i])
          });
          formData.append(n, input.files[i]);
        }

        self.$emit("request", self.factory(formData, files));
      }
    },
    factory(formData, files) {
      let self = this;
      return {
        limit: this.limit,
        formData: formData,
        files: files,
        send(url, data, callback) {
          if (typeof data === "object" && data !== null) {
            for (var k in data) {
              this.formData.append(k, data[k]);
            }
          }
          var request = new XMLHttpRequest();
          if (typeof callback === "function") {
            request.onreadystatechange = function () {
              if (this.readyState == 4 && this.status == 200) {
                self.$refs.uploadField.value = null;
                callback(this.response, this.responseType);
              }
            };
            request.open("POST", url, true);
          } else {
            request.open("POST", url);
          }

          request.send(this.formData);
        },
      };
    },
  },
};
</script>