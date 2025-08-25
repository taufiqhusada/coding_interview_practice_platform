<template>
  <nav class="navbar navbar-light bg-light">
    <div class="container d-flex justify-content-between" style="height: 40px;">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <!-- <img src="/images/minimalist_interview_logo.png" width="33" height="33"
          class="d-inline-block align-top rounded-circle" alt=""> -->
        <b class="site-title">Think-Aloud Practice in Technical Interview</b>
      </a>
      <div class="navbar-items d-flex" style="margin-right: 80px;">
        <a class="nav-link" :class="{ 'current-link': currentPage === 'simulation' }" href="/">
          Simulation
        </a>
        <!-- <a class="nav-link" :class="{ 'current-link': currentPage === 'guidedPractice' }" href="/guidedSimulation">
          Guided Practice
        </a> -->
        <a class="nav-link" :class="{ 'current-link': currentPage === 'feedback' }" href="/feedback">
          Feedback
        </a>
        <a class="nav-link" :class="{ 'current-link': currentPage === 'example' }" href="/example">
          Example
        </a>
        <a v-show="false" class="nav-link" :class="{ 'current-link': currentPage === 'comparison' }" href="/comparison">
          4. Comparison
        </a>
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
  /* border-bottom: 2px solid #007bff; */
  border-bottom: 2px solid rgb(86, 180, 233);
}
</style>
