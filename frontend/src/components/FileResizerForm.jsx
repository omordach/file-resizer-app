import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import ReCAPTCHA from "react-google-recaptcha";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";

export default function FileResizerForm() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState("Image");
  const [width, setWidth] = useState("");
  const [height, setHeight] = useState("");
  const [quality, setQuality] = useState("ebook");
  const [captchaToken, setCaptchaToken] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setMessage("");
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleCaptchaChange = (value) => {
    setCaptchaToken(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return setMessage("⚠️ Please select a file.");
    if (!captchaToken) return setMessage("⚠️ Please complete the captcha.");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", fileType);
    formData.append("width", width);
    formData.append("height", height);
    formData.append("quality", quality);
    formData.append("captcha_token", captchaToken);

    setIsLoading(true);
    try {
      const response = await fetch("/api/process", { method: "POST", body: formData });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = file.name;
        link.click();
        setMessage("✅ File processed successfully.");
      } else {
        setMessage("❌ Error processing file.");
      }
    } catch (error) {
      console.error(error);
      setMessage("❌ An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted p-4">
      <Card className="w-full max-w-md">
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-center">Resize File</h2>

          <div
            {...getRootProps()}
            className={`border-2 border-dashed p-4 text-center rounded cursor-pointer ${
              isDragActive ? "bg-gray-100" : "bg-white"
            }`}
          >
            <input {...getInputProps()} />
            {file ? (
              <p>Selected file: {file.name}</p>
            ) : (
              <p>Drag 'n' drop a file here, or click to select</p>
            )}
          </div>

          <div>
            <Label>File Type</Label>
            <Select value={fileType} onValueChange={setFileType}>
              <SelectTrigger>
                <SelectValue placeholder="Select type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Image">Image</SelectItem>
                <SelectItem value="PDF">PDF</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {fileType === "Image" && (
            <>
              <div>
                <Label htmlFor="width">Width</Label>
                <Input id="width" type="number" value={width} onChange={(e) => setWidth(e.target.value)} />
              </div>
              <div>
                <Label htmlFor="height">Height</Label>
                <Input id="height" type="number" value={height} onChange={(e) => setHeight(e.target.value)} />
              </div>
            </>
          )}

          {fileType === "PDF" && (
            <div>
              <Label>PDF Quality</Label>
              <Select value={quality} onValueChange={setQuality}>
                <SelectTrigger>
                  <SelectValue placeholder="Select quality" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="screen">screen</SelectItem>
                  <SelectItem value="ebook">ebook</SelectItem>
                  <SelectItem value="printer">printer</SelectItem>
                  <SelectItem value="prepress">prepress</SelectItem>
                </SelectContent>
              </Select>
            </div>
          )}

          <div>
            <ReCAPTCHA sitekey="6Ld_rTsrAAAAAL3WCWzTJnrRYDdPKxbKvkJR1B1r" onChange={handleCaptchaChange} />
          </div>

          <Button className="w-full mt-2" onClick={handleSubmit} disabled={isLoading}>
            {isLoading ? "Processing..." : "Process"}
          </Button>

          {message && <p className="text-center text-sm text-muted-foreground">{message}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
