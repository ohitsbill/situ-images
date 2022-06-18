const chooseFile = document.getElementById("file");
const imgPreview = document.getElementById("img-preview");
const place = document.getElementById("place");
const descTxt = document.querySelector(".descTxt");
const fileTxt = document.querySelector(".file-txt");

chooseFile.addEventListener("change", function () {
  getImgData();
  descTxt.classList.add("hide");
  fileTxt.classList.add("show");
  place.removeAttribute("disabled");
});

function getImgData() {
  const files = chooseFile.files[0];
  if (files) {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(files);
    fileReader.addEventListener("load", function () {
      imgPreview.style.display = "block";
      imgPreview.innerHTML = '<img src="' + this.result + '" />';
    });
  }
}

const file = document.querySelector('#file');
file.addEventListener('change', (e) => {
  // Get the selected file
  const [file] = e.target.files;
  // Get the file name and size
  const { name: fileName, size } = file;
  // Convert size in bytes to kilo bytes
  const fileSize = (size / 1000).toFixed(2);
  // Set the text content
  const fileNameAndSize = `${fileName} - ${fileSize}KB`;
  document.querySelector('.file-name').textContent = fileNameAndSize;
});
