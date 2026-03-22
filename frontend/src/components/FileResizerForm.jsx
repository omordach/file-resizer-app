import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import ReCAPTCHA from "react-google-recaptcha";
import { Loader2 } from "lucide-react";
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
  const [message, setMessage] = useState({ text: "", type: "" });
  const [isLoading, setIsLoading] = useState(false);

  const onDrop = (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    setFile(uploadedFile);
    setMessage({ text: "", type: "" });

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
    if (!file) return setMessage({ text: "⚠️ Please select a file.", type: "error" });
    if (!captchaToken) return setMessage({ text: "⚠️ Please complete the captcha.", type: "error" });

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
        setMessage({ text: "✅ File processed successfully.", type: "success" });
      } else {
        setMessage({ text: "❌ Error processing file.", type: "error" });
      }
    } catch (error) {
      console.error(error);
      setMessage({ text: "❌ An unexpected error occurred.", type: "error" });
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setMessage({ text: "", type: "" });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted p-4">
      <Card className="w-full max-w-md">
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-center">Resize File</h2>

          <div
            {...getRootProps()}
            className={`border-2 border-dashed p-4 text-center rounded cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${
              isDragActive ? "bg-gray-100" : "bg-white"
            }`}
          >
            <input {...getInputProps()} />
            {file ? <p>Selected file: {file.name}</p> : <p>Drag 'n' drop a file here, or click to select</p>}
            <p className="text-xs text-muted-foreground mt-1">Supported: JPG, PNG, PDF (max 30MB)</p>
          </div>

          {file && file.type.startsWith("image/") && (
            <img src={URL.createObjectURL(file)} alt="Preview" className="mt-2 rounded shadow" />
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

          <div className="flex space-x-2 mt-2">
            <Button className="w-full" onClick={handleSubmit} disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />}
              {isLoading ? "Processing..." : "Process"}
            </Button>
            {file && <Button variant="secondary" onClick={handleClear}>Clear File</Button>}
          </div>

          {message.text && (
            <p
              aria-live="polite"
              className={`text-center text-sm font-medium ${
                message.type === "error" ? "text-destructive" : "text-green-600"
              }`}
            >
              {message.text}
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
