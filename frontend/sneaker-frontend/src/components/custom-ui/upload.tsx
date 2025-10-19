import { useState, useRef } from "react";

import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";

type Prediction = {
    label: string
    confidence: number
}

type PredictionResult = {
    predictions: Prediction[]
}

export function Upload(){
    const [preview, setPreview] = useState<string | null>(null)
    const [prediction, setPrediction] = useState<PredictionResult | null>(null)
    const [loading, setLoading] = useState(false)
    const inputRef = useRef<HTMLInputElement | null>(null)  

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if(file){
            setPreview(URL.createObjectURL(file))
        }
    }

    const handleUpload = async () => {
        const file = inputRef.current?.files?.[0]
        if(!file) return

        const formData = new FormData()
        formData.append("file", file)
        setLoading(true)

        try{
            const res = await fetch("https://sneaker-ai-backend.onrender.com/predict", {
                method: "POST",
                body: formData,
        })
        const data = await res.json()
        setPrediction(data)
        console.log("Prediction result:", data)
        }catch(err){
            console.error("Error prediction sneaker:", err)
        }finally{    
            setLoading(false)
        }
    }

    return (
        <div className="flex flex-row gap-4">
            <div className="flex flex-col items-center  max-w-xs">
                 {preview && (
                    <img
                        src={preview}
                        alt="Preview"
                        className="mt-4 rounded-md p-4 bg-white shadow"
                    />
                )}
                <div className="flex flex-col w-full gap-4 my-4">
                    <Label htmlFor="picture">Upload Image</Label>
                    <Input id="image" type="file" onChange={handleImageChange} ref={inputRef}/>
                    <Button onClick={handleUpload} disabled={loading}>
                        {loading ? "Predicting..." : "Upload Image"}
                    </Button>
                </div>
            
            </div>
           

            {prediction && prediction.predictions && (
                <div className="mt-4 p-4 border rounded w-md bg-gray-50 max-w-xs">
                    <p><strong>Top Predictions</strong></p>
                    <p><strong>Brand: </strong>{prediction.predictions[0].label}</p>
                    <p><strong>Confidence: </strong>{prediction.predictions[0].confidence}%</p>

                    <hr className="my-2" />
                    <p className="font-semibold">Other Predictions:</p>
                    <ul className="list-disc list-inside text-sm text-gray-700">
                    {prediction.predictions.slice(1).map((item: Prediction, index: number) => (
                        <li key={index}>
                        {item.label} — {item.confidence.toFixed(2)}%
                        </li>
                    ))}
                    </ul>
                </div>
            )}
        </div>
    )
}