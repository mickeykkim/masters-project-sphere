<template>
  <v-toolbar fixed class="sunset" dark>
    <v-toolbar-title class="mr-4">
      <router-link
        class="home"
        tag="div"
        :to="{
          name: 'root'
        }">
        <p>Song Share</p>
      </router-link>
    </v-toolbar-title>
    <v-toolbar-items>
      <v-btn class="button-label"
        flat dark
        :to="{
          name: 'songs'
        }">
        <v-icon
          medium
          light
          left
        >library_music</v-icon>
        Browse
      </v-btn>
    </v-toolbar-items>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn flat dark class="button-label"
          v-if="!$store.state.isUserLoggedIn"
          :to="{
            name: 'login'
          }">
          <v-icon
            medium
            light
            left
          >person</v-icon>
          Login
        </v-btn>
        <v-btn flat dark class="button-label"
          v-if="!$store.state.isUserLoggedIn"
          :to="{
            name: 'register'
          }">
          <v-icon
            medium
            light
            left
          >person_add</v-icon>
          Sign Up
        </v-btn>
        <v-btn flat dark class="button-label"
          v-if="$store.state.isUserLoggedIn"
          @click="logout">
          <v-icon
            medium
            light
            left
          >exit_to_app</v-icon>
          LogOut
        </v-btn>
      </v-toolbar-items>
    <!-- </v-toolbar-items> -->
  </v-toolbar>
</template>

<script>
export default {
  methods: {
    logout () {
      this.$store.dispatch('setToken', null)
      this.$store.dispatch('setUser', null)
      this.$router.push({
        name: 'root'
      })
    }
  }
}
</script>

<style scoped>
p {
  line-height: 34px;
}
div {
  display: flex;
  height: 36px;
}
img {
  margin-right: 10px;
}
.home {
  cursor: pointer;
}
.home:hover {
  color: rgb(255, 255, 255);
}
.sunset {
  color: #141414;
  background: rgb(168,108,209);
  background: linear-gradient(90deg, rgba(168,108,209,1) 0%, rgba(253,29,29,1) 50%, rgba(252,176,69,1) 100%);
}
.button-label {
  color: #141414;
  background: rgba(255,255,255,0.1);
}
</style>