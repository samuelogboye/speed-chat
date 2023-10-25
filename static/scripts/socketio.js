document.addEventListener("DOMContentLoaded", () => {
  var socket = io.connect("http://" + document.domain + ":" + location.port);

  let group = "lounge";
  joingroup("lounge");
  // Display incoming message
  socket.on("message", (data) => {
    const p = document.createElement("p");
    const span_username = document.createElement("span");
    const span_timestamp = document.createElement("span");
    const br = document.createElement("br");

    if (data.username) {
      span_username.innerHTML = data.username;
      span_timestamp.innerHTML = data.time_stamp;
      p.innerHTML =
        span_username.outerHTML +
        br.outerHTML +
        data.msg +
        br.outerHTML +
        span_timestamp.outerHTML +
        br.outerHTML;
      document.querySelector("#display-message-section").append(p);
    } else {
      printSysMsg(data.msg);
    }
  });

  socket.on("some-event", (data) => {
    console.log(data);
  });

  // Send message
  document.querySelector("#send_message").onclick = () => {
    socket.send({
      msg: document.querySelector("#user_message").value,
      username: username,
      group: group,
    });
    // Clear input area
    document.querySelector("#user_message").value = "";
  };

  // group selection
  document.querySelectorAll(".select-group").forEach((p) => {
    p.onclick = () => {
      let newgroup = p.innerHTML;
      if (newgroup == group) {
        msg = `You are already in ${group} group.`;
        printSysMsg(msg);
      } else {
        leavegroup(group);
        joingroup(newgroup);
        group = newgroup;
      }
    };
  });

  // Leave group
  function leavegroup(group) {
    socket.emit("leave", { username: username, group: group });
  }

  // Join group
  function joingroup(group) {
    socket.emit("join", { username: username, group: group });
    // Clear message area
    document.querySelector("#display-message-section").innerHTML = "";
    // Autofocus on text box
    document.querySelector("#user_message").focus();
  }

  // Print system messages
  function printSysMsg(msg) {
    const p = document.createElement("p");
    p.innerHTML = msg;
    document.querySelector("#display-message-section").append(p);
  }
});
