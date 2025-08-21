import { toggleTheme } from "../../js/theme.js";


const editPic = document.getElementsByClassName("edit-pic")[0];
  if (editPic) {
    editPic.addEventListener("click", toggleTheme);
  }