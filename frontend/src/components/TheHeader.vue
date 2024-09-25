<template>
  <nav class="navbar navbar-light bg-light shadow">
    <div class="container d-flex justify-content-between">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <img src="/images/minimalist_interview_logo.png" width="33" height="33"
          class="d-inline-block align-top rounded-circle" alt="">
        <b class="site-title">Coding Interview Practice</b>
      </a>
      <div class="navbar-items d-flex">
        <a class="nav-link" :class="{ 'current-link': currentPage === 'simulation' }" href="/">
          1. Simulation
        </a>
        <a class="nav-link" :class="{ 'current-link': currentPage === 'feedback' }" href="/feedback">
          2. Assessment
        </a>
        <a class="nav-link" :class="{ 'current-link': currentPage === 'example' }" href="/example">
          3. Example
        </a>
        <!-- <a class="nav-link" :class="{ 'current-link': currentPage === 'comparison' }" href="/comparison">
          4. Comparison
        </a> -->
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    currentPage: {
      type: String,
      default: "simulation",
    },
  },
};
</script>

<style>
.site-title {
  display: flex;
  align-self: center;
  font-weight: bold;
  margin-left: 15px;
  font-size: smaller;
}

.navbar-items {
  display: flex;
  align-items: center;
}

.navbar-items a {
  margin-left: 15px;
  text-decoration: none;
  color: #000;
  font-weight: bold;
  transition: color 0.3s ease-in-out;
}

/* Non-active link hover effect */
.navbar-items a:hover {
  text-decoration: underline;
  color: #007bff;
}

/* Current link styling */
.current-link {
  color: #007bff;
  border-bottom: 2px solid #007bff;
}
</style>
