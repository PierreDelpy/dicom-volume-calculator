const dicomUploader = Vue.createApp({
  data() {
    return {
      pixelsAboveThreshold: null, //Task 1.B
      extractedPixelData: null, //Task 2.C
      calculatedVoxelVolume: null, // computed voxel volume in mm^3
      calculatedVolume: null, // computed volume in mm^3
      uploadErrorMessage: null // error message if necessary
    };
  },

  methods: {
    // Trigger Upload when a file is provided
    dicomFileUpload(dicomFileEvent) {
      //create POST body
      const uploadFormData = new FormData();
      uploadFormData.append("dicom_file", dicomFileEvent.target.files[0]);

      //execute POST file to backend
      fetch("http://localhost:5000/upload", {
        method: "POST",
        body: uploadFormData
      })
        .then(response => response.json()) //store result in json
        .then(result => {
          if (result.volume !== undefined) {
            this.pixelsAboveThreshold = result.pixels_above_threshold;
            this.extractedPixelData = result.extracted_pixel_data;
            this.calculatedVoxelVolume = result.voxel_volume;
            this.calculatedVolume = result.volume;
            this.uploadErrorMessage = null;
          } else {
            this.uploadErrorMessage = result.error || "No volume returned.";
          }
        })
        .catch(fetchError => {
          this.uploadErrorMessage = "Upload failed: " + fetchError.message;
          this.calculatedVolume = null;
        });
    }
  }
});
dicomUploader.mount("#dicomUploader");
