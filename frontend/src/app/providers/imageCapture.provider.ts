import {Injectable} from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class ImageCaptureProvider {

  /**
   * @param stream
   */
  buildVideo(stream: any) {

    return new Promise((resolve, reject) => {
      const vid = document.createElement('video');
      vid.srcObject = stream;
      vid.play().then(() => {
        setTimeout(() => {
          this.buildCanvas(stream, vid, (blob: Blob) => {
            resolve(blob);
            this.removeTracks(stream)

          })
        }, 1000)
      })
    })

  }

  /**
   * @param stream
   * @param vidElement
   * @param callback
   */
  buildCanvas(stream: any, vidElement: any, callback = (blob: Blob) => {}) {
    const canvas = document.createElement('canvas');
    const canvasCtx = canvas.getContext('2d');
    canvasCtx!.drawImage(vidElement, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => callback(blob as Blob));
  }

  /**
   * @param stream
   */
  removeTracks(stream: any) {
    stream.getTracks().forEach((track: MediaStreamTrack) => {
      track.stop();
    })
  }
}
