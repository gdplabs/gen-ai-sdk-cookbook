import {
  useDispatchAction,
  ComponentRenderer,
  type CatalogComponent,
} from '@a2ui-sdk/react/0.8'
import type { ButtonComponentProps } from '@a2ui-sdk/types/0.8/standard-catalog'

export const CustomButtonComponent: CatalogComponent = ({
  surfaceId,
  componentId,
  ...props
}) => {
  const { child, action, primary } = props as ButtonComponentProps
  const dispatchAction = useDispatchAction()

  const handleClick = () => {
    if (action) {
      dispatchAction(surfaceId, componentId, action)
    }
  }

  return (
    <button onClick={handleClick} className={`${primary ? 'bg-blue-500 text-white' : 'bg-transparent border border-gray-300 text-gray-700'} p-2 rounded-md cursor-pointer`}>
      {child && <ComponentRenderer surfaceId={surfaceId} componentId={child} />}
    </button>
  )
}