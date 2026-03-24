import React, { useState, useEffect } from "react";
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
  const [previewUrl, setPreviewUrl] = useState(null);


  useEffect(() => {
    if (!file || !file.type.startsWith("image/")) {
      setPreviewUrl(null);
      return;
    }
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);

    // free memory when ever this component is unmounted
    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  const onDrop = (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    setFile(uploadedFile);
    setMessage("");

    // Auto-detect file type
    if (uploadedFile.type.startsWith("image/")) {
      setFileType("Image");
    } else if (uploadedFile.type === "application/pdf") {
      setFileType("PDF");
    }
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

        // Clean up the object URL to avoid memory leaks
        setTimeout(() => URL.revokeObjectURL(url), 100);

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

  const handleClear = () => {
    setFile(null);
    setMessage("");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted p-4">
      <Card className="w-full max-w-md">
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-center">Resize File</h2>

          <div {...getRootProps()} className={`border-2 border-dashed p-6 text-center rounded-lg transition-colors cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${isDragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:bg-muted/50 bg-background"}`}>
            <input {...getInputProps()} aria-label="File upload dropzone" />
            {file ? (
              <p className="font-medium text-primary">
                {file.name} <span className="text-muted-foreground font-normal">({(file.size / 1024 / 1024).toFixed(2)} MB)</span>
              </p>
            ) : (
              <p className="font-medium">Drag 'n' drop a file here, or click to select</p>
            )}
            <p className="text-xs text-muted-foreground mt-1">Supported: JPG, PNG, PDF (max 30MB)</p>
          </div>

          {file && file.type.startsWith("image/") && (
            <img src={previewUrl} alt={`Preview of ${file.name}`} className="mt-2 rounded-md shadow-sm max-h-48 object-contain mx-auto" />
          )}

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
            <div className="flex space-x-4">
              <div className="flex-1">
                <Label htmlFor="width">Width (px)</Label>
                <Input id="width" type="number" placeholder="Auto" value={width} onChange={(e) => setWidth(e.target.value)} />
              </div>
              <div className="flex-1">
                <Label htmlFor="height">Height (px)</Label>
                <Input id="height" type="number" placeholder="Auto" value={height} onChange={(e) => setHeight(e.target.value)} />
              </div>
            </div>
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

          <div className="flex space-x-2 mt-4">
            <Button className="w-full transition-all" onClick={handleSubmit} disabled={isLoading || !file}>
              {isLoading ? "Processing..." : "Process File"}
            </Button>
            {file && (
              <Button variant="outline" onClick={handleClear} aria-label="Clear selected file" title="Clear file" className="px-3 hover:bg-destructive/10 hover:text-destructive">
                Clear
              </Button>
            )}
          </div>

          {message && <p className="text-center text-sm text-muted-foreground">{message}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
